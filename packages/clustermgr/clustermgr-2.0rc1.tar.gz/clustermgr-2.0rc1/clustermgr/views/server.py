# -*- coding: utf-8 -*-

import os
# import uuid

from flask import Blueprint, render_template, redirect, url_for, flash, \
    request
from flask_login import login_required

from clustermgr.extensions import db
from clustermgr.models import Server, AppConfiguration

from index import getLdapConn

from clustermgr.forms import ServerForm, InstallServerForm, \
    SetupPropertiesLastForm
from clustermgr.tasks.cluster import collect_server_details
from clustermgr.core.remote import RemoteClient, ClientNotSetupException
from ..core.license import license_required
from ..core.license import license_reminder
from ..core.license import prompt_license

from clustermgr.core.utils import parse_setup_properties, \
    write_setup_properties_file, get_setup_properties


server_view = Blueprint('server', __name__)
server_view.before_request(prompt_license)
server_view.before_request(license_required)
server_view.before_request(license_reminder)


def sync_ldap_passwords(password):
    non_primary_servers = Server.query.filter(
        Server.primary_server.isnot(True)).all()
    for server in non_primary_servers:
        server.ldap_password = password
    db.session.commit()


@server_view.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Route for URL /server/. GET returns ServerForm to add a server,
    POST accepts the ServerForm, validates and creates a new Server object
    """
    appconfig = AppConfiguration.query.first()
    if not appconfig:
        flash("Kindly set default values for the application before adding"
              " servers.", "info")
        return redirect(url_for('index.app_configuration', next="/server/"))

    form = ServerForm()
    header = "New Server"
    primary_server = Server.query.filter(
        Server.primary_server.is_(True)).first()

    if primary_server:
        del form.ldap_password
        del form.ldap_password_confirm
    else:
        header = "New Server - Primary Server"

    if form.validate_on_submit():
        
        server = Server()
        server.hostname = form.hostname.data.strip()
        server.ip = form.ip.data.strip()
        server.mmr = False
        
        
        c = RemoteClient(server.hostname, server.ip)
        try:
            c.startup()
        except:
            flash("SSH connection to {} failed. Please check if your pub key is "
                "asdded to /root/.ssh/authorized_keys on this server".format(
                                                    server.hostname))
            
            return render_template('new_server.html',
                       form=form,
                       header=header,
                       server_id=None)
        
        if primary_server:
            server.ldap_password = primary_server.ldap_password
        else:
            server.ldap_password = form.ldap_password.data.strip()
            server.primary_server = True
        
        if not server.hostname == appconfig.nginx_host:
            db.session.add(server)
            db.session.commit()
            # start the background job to get system details
            collect_server_details.delay(server.id)
            return redirect(url_for('index.home'))

        else:
            flash("Load balancer can't be used as gluu server", 'danger')


    return render_template('new_server.html',
                           form=form,
                           header=header,
                           server_id=None)


@server_view.route('/edit/<int:server_id>/', methods=['GET', 'POST'])
@login_required
def edit(server_id):
    server = Server.query.get(server_id)
    if not server:
        flash('There is no server with the ID: %s' % server_id, "warning")
        return redirect(url_for('index.home'))

    form = ServerForm()
    header = "Update Server Details"
    if server.primary_server:
        header = "Update Primary Server Details"
        if request.method == 'POST' and not form.ldap_password.data.strip():
            form.ldap_password.data = '**dummy**'
            form.ldap_password_confirm.data = '**dummy**'
    else:
        del form.ldap_password
        del form.ldap_password_confirm

    if form.validate_on_submit():
        server.hostname = form.hostname.data.strip()
        server.ip = form.ip.data.strip()
        if server.primary_server and form.ldap_password.data != '**dummy**':
            server.ldap_password = form.ldap_password.data.strip()
            sync_ldap_passwords(server.ldap_password)
        db.session.commit()
        # start the background job to get system details
        collect_server_details.delay(server.id)
        return redirect(url_for('index.home'))

    form.hostname.data = server.hostname
    form.ip.data = server.ip
    if server.primary_server:
        form.ldap_password.data = server.ldap_password

    return render_template('new_server.html', form=form, header=header)


def remove_provider_from_consumer_f(consumer_id, provider_addr):
    server = Server.query.get(consumer_id)

    # Make ldap connection
    ldp = getLdapConn(server.hostname, "cn=config", server.ldap_password)

    success = False

    # If connection was established try to delete provider
    if ldp:
        r = ldp.removeProvider("ldaps://{0}:1636".format(provider_addr))
        if r:
            if ldp.conn.result['description'] == 'success':
                flash('Provder {0} from {1} is removed'.format(
                    provider_addr, server.hostname), 'success')
                success = True

    if not success:
        if ldp:
            flash("Removing provider was failed: {0}".format(
                  ldp.conn.result['description']), "danger")
        else:
            flash("Can't connect to LDAP server", "danger")


@server_view.route('/removeprovider/<consumer_id>/<provider_addr>')
def remove_provider_from_consumer(consumer_id, provider_addr):
    """This view delates provider from consumer"""

    remove_provider_from_consumer_f(consumer_id, provider_addr)

    return redirect(url_for('index.multi_master_replication'))


@server_view.route('/remove/<int:server_id>/')
@login_required
def remove(server_id):
    appconfig = AppConfiguration.query.first()
    server = Server.query.filter_by(id=server_id).first()
    provider_addr = server.ip if appconfig.use_ip else server.hostname

    setup_prop = get_setup_properties()

    if server.mmr:
        if setup_prop['ldap_type'] == 'openldap':
            db.session.delete(server)

            # remove its corresponding syncrepl configs from other servers
            consumers = Server.query.filter(Server.id.isnot(server_id)).all()
            for consumer in consumers:
                remove_provider_from_consumer_f(consumer.id, provider_addr)
        else:

            return redirect(url_for('cluster.opendj_disable_replication',
                                    server_id=server_id, removeserver=True,
                                    next='dashboard',
                                    ))
    else:
        db.session.delete(server)

    db.session.commit()
    # TODO LATER perform checks on ther flags and add their cleanup tasks

    flash("Server {0} is removed.".format(server.hostname), "success")
    return redirect(url_for('index.home'))


@server_view.route('/installgluu/<int:server_id>/', methods=['GET', 'POST'])
@login_required
def install_gluu(server_id):
    """Gluu server installation view. This function creates setup.properties
    file and redirects to install_gluu_server which does actual installation.
    """

    # If current server is not primary server, first we should identify
    # primary server. If primary server is not installed then redirect
    # to home to install primary.
    pserver = Server.query.filter_by(primary_server=True).first()
    if not pserver:
        flash("Please identify primary server before starting to install Gluu "
              "Server.", "warning")
        return redirect(url_for('index.home'))

    server = Server.query.get(server_id)

    # We need os type to perform installation. If it was not identified,
    # return to home and wait until it is identifed.
    if not server.os:
        flash("Server OS version hasn't been identified yet. Checking Now",
              "warning")
        collect_server_details.delay(server_id)
        return redirect(url_for('index.home'))

    # If current server is not primary server, and primary server was installed,
    # start installation by redirecting to cluster.install_gluu_server
    if not server.primary_server:
        return redirect(url_for('cluster.install_gluu_server',
                                server_id=server_id))

    # If we come up here, it is primary server and we will ask admin which
    # components will be installed. So prepare form by InstallServerForm
    appconf = AppConfiguration.query.first()
    form = InstallServerForm()

    # We don't require these for server installation. These fields are required
    # for adding new server.
    del form.hostname
    del form.ip_address
    del form.ldap_password

    header = 'Install Gluu Server on {0}'.format(server.hostname)

    # Get default setup properties.
    setup_prop = get_setup_properties()

    setup_prop['hostname'] = appconf.nginx_host
    setup_prop['ip'] = server.ip
    setup_prop['ldapPass'] = server.ldap_password

    # If form is submitted and validated, create setup.properties file.
    if form.validate_on_submit():
        setup_prop['countryCode'] = form.countryCode.data.strip()
        setup_prop['state'] = form.state.data.strip()
        setup_prop['city'] = form.city.data.strip()
        setup_prop['orgName'] = form.orgName.data.strip()
        setup_prop['admin_email'] = form.admin_email.data.strip()
        setup_prop['inumOrg'] = form.inumOrg.data.strip()
        setup_prop['inumAppliance'] = form.inumAppliance.data.strip()
        for o in ('installOxAuth',
                  'installOxTrust',
                  'installLDAP',
                  'installHTTPD',
                  'installJce',
                  'installSaml',
                  'installAsimba',
                  # 'installCas',
                  'installOxAuthRP',
                  'installPassport',
                  'ldap_type',
                  ):
            setup_prop[o] = getattr(form, o).data

        write_setup_properties_file(setup_prop)

        # Redirect to cluster.install_gluu_server to start installation.
        return redirect(url_for('cluster.install_gluu_server',
                                server_id=server_id))

    # If this view is requested, rather than post, display form to
    # admin to determaine which elements to be installed.
    if request.method == 'GET':
        form.countryCode.data = setup_prop['countryCode']
        form.state.data = setup_prop['state']
        form.city.data = setup_prop['city']
        form.orgName.data = setup_prop['orgName']
        form.admin_email.data = setup_prop['admin_email']
        form.inumOrg.data = setup_prop['inumOrg']
        form.inumAppliance.data = setup_prop['inumAppliance']

        for o in ('installOxAuth',
                  'installOxTrust',
                  'installLDAP',
                  'installHTTPD',
                  'installJce',
                  'installSaml',
                  'installAsimba',
                  # 'installCas',
                  'installOxAuthRP',
                  'installPassport',
                  'ldap_type',
                  ):
            getattr(form, o).data = setup_prop.get(o, '')

        # if appconf.gluu_version < '3.1.2':
        #     print "removeing opendj"
        #     form.ldap_type.choices.remove(('opendj', 'OpenDJ'))
        #     form.ldap_type.data = 'openldap'

    setup_properties_form = SetupPropertiesLastForm()

    return render_template('new_server.html',
                           form=form,
                           server_id=server_id,
                           setup_properties_form=setup_properties_form,
                           header=header)


@server_view.route('/uploadsetupproperties/<int:server_id>', methods=['POST'])
def upload_setup_properties(server_id):
    setup_properties_form = SetupPropertiesLastForm()
    if setup_properties_form.upload.data and \
            setup_properties_form.validate_on_submit():

        f = setup_properties_form.setup_properties.data

        setup_prop = parse_setup_properties(f.stream)

        print setup_prop

        for rf in ('oxauthClient_encoded_pw',
                   'encoded_ldap_pw',
                   'scim_rp_client_jks_pass',
                   'passport_rp_client_jks_pass',
                   'asimbaJksPass',
                   'encoded_ox_ldap_pw',
                   'oxauthClient_pw',
                   'encoded_shib_jks_pw',
                   'encoded_openldapJksPass',
                   'pairwiseCalculationSalt',
                   'openldapKeyPass',
                   'pairwiseCalculationKey',
                   'httpdKeyPass',
                   'scim_rs_client_jks_pass_encoded',
                   'encode_salt',
                   'scim_rs_client_jks_pass',
                   'shibJksPass',
                   ):
            del setup_prop[rf]

        appconf = AppConfiguration.query.first()
        server = Server.query.get(server_id)

        setup_prop['hostname'] = appconf.nginx_host
        setup_prop['ip'] = server.ip
        setup_prop['ldapPass'] = server.ldap_password

        write_setup_properties_file(setup_prop)

        flash("Setup properties file has been uploaded sucessfully. ",
              "success")

        return redirect(url_for('cluster.install_gluu_server',
                                server_id=server_id))
    else:
        flash("Please upload valid setup properties file", "danger")

        return redirect(url_for('server.install_gluu', server_id=server_id))


@server_view.route('/editslapdconf/<int:server_id>/', methods=['GET', 'POST'])
@login_required
def edit_slapd_conf(server_id):
    """This view  provides editing of slapd.conf file before depoloyments."""

    server = Server.query.get(server_id)
    appconf = AppConfiguration.query.first()

    # If there is no server with server_id return to home
    if not server:
        flash("No such server.", "warning")
        return redirect(url_for('index.home'))

    if not server.gluu_server:
        chroot = '/'
    else:
        chroot = '/opt/gluu-server-' + appconf.gluu_version

    # slapd.conf file will be downloaded from server. Make ssh connection
    # and download it
    c = RemoteClient(server.hostname, ip=server.ip)
    try:
        c.startup()
    except ClientNotSetupException as e:
        flash(str(e), "danger")
        return redirect(url_for('index.home'))

    slapd_conf_file = os.path.join(chroot, 'opt/symas/etc/openldap/slapd.conf')

    if request.method == 'POST':

        config = request.form.get('conf')
        r = c.put_file(slapd_conf_file, config)
        if not r[0]:
            flash("Cant' saved to server: {0}".format(r[1]), "danger")
        else:
            flash('File {0} was saved on {1}'.format(slapd_conf_file,
                                                     server.hostname))
            return redirect(url_for('index.home'))

    # After editing, slapd.conf file will be uploaded to server via ssh
    r = c.get_file(slapd_conf_file)

    if not r[0]:
        flash("Cant't get file {0}: {1}".format(slapd_conf_file, r[1]),
              "success")
        return redirect(url_for('index.home'))

    config = r[1].read()

    return render_template('conf_editor.html', config=config,
                           hostname=server.hostname)
