try:
    from flask_wtf import FlaskForm
except ImportError:
    from flask_wtf import Form as FlaskForm
from wtforms import StringField, SelectField, BooleanField, IntegerField, \
    PasswordField, RadioField, SubmitField, validators, TextAreaField, \
    HiddenField
from wtforms.validators import DataRequired, AnyOf, \
    ValidationError, URL, IPAddress, Email, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class AppConfigForm(FlaskForm):
    versions = ['3.1.2']
    gluu_version = SelectField('Gluu Server Version',
                               choices=[(v, v) for v in versions])
    # use_ip = BooleanField('Use IP Address in place of Hostname for replication')
    # replication_dn = StringField('Replication Manager DN', validators=[
    #    DataRequired(),
    #    Regexp('^[a-zA-Z][a-zA-Z ]*[a-zA-Z]$',
    #           message="Only alphabets and space allowed; cannot end with space.")])  # noqa
    replication_pw = PasswordField('Replication Manager Password', validators=[
        DataRequired(), validators.EqualTo(
            'replication_pw_confirm', message='Passwords must match')])
    replication_pw_confirm = PasswordField(
        'Re-enter Password', validators=[DataRequired()])
    nginx_host = StringField('Load Balancer Hostname', validators=[DataRequired()])

    nginx_ip = StringField('Load Balancer IP Address', validators=[DataRequired()])

    # purge_age_day = SelectField(choices=[(str(d), str(d)) for d in range(0, 31)])
    # purge_age_hour = SelectField(choices=[(str(h), str(h)) for h in range(0, 25)], default="24")
    # purge_age_min = SelectField(choices=[(str(m), str(m)) for m in range(0, 60)])

    # purge_interval_day = SelectField(choices=[(str(d), str(d)) for d in range(0, 31)], default="1")
    # purge_interval_hour = SelectField(choices=[(str(h), str(h)) for h in range(0, 25)])
    # purge_interval_min = SelectField(choices=[(str(m), str(m)) for m in range(0, 60)])

    # admin_email = StringField("Admin Email", validators=[Optional(), Email("Please enter valid email address")])

    modify_hosts =  BooleanField('Add IP Addresses and hostnames to /etc/hosts file on each server')

    update = SubmitField("Update Configuration")


class SchemaForm(FlaskForm):
    schema = FileField(validators=[
        FileRequired(),
        FileAllowed(
            ['schema'],
            'Upload only Openldap Schema files with .schema extension.')
    ])
    upload = SubmitField("Upload Schema")


class SetupPropertiesLastForm(FlaskForm):
    setup_properties = FileField(validators=[
        FileRequired(),
        FileAllowed(
            ['last'],
            'Upload only setup.properties.last files with .last extension.')
    ])
    upload = SubmitField("Upload Setup Properties")


class LDIFForm(FlaskForm):
    ldif = FileField(validators=[
        FileRequired(),
        FileAllowed(
            ['ldif'], 'Upload OpenLDAP slapcat exported ldif files only!')
    ])


class KeyRotationForm(FlaskForm):
    interval = IntegerField("Rotation Interval", validators=[DataRequired()])
    type = RadioField(
        "Rotation Type",
        choices=[("oxeleven", "oxEleven",), ("jks", "JKS")],
        validators=[AnyOf(["oxeleven", "jks"])],
    )
    oxeleven_url = StringField("oxEleven URL")
    oxeleven_token = PasswordField("oxEleven Token")
    inum_appliance = StringField("Inum Appliance", validators=[DataRequired()])
    gluu_server = BooleanField(
        'Installed inside chroot-ed Gluu Server', default=True)
    gluu_version = SelectField('Gluu Server Version', choices=[
        ('3.0.1', '3.0.1'),
        ('3.0.2', '3.0.2'),
    ])

    def validate_oxeleven_url(form, field):
        if not field.data and form.type.data == "oxeleven":
            raise ValidationError("This field is required if oxEleven is "
                                  "selected as rotation type")

    def validate_oxeleven_token(form, field):
        if not field.data and form.type.data == "oxeleven":
            raise ValidationError("This field is required if oxEleven is "
                                  "selected as rotation type")


class LoggingServerForm(FlaskForm):
    # mq_host = StringField("Hostname", validators=[DataRequired()])
    # mq_port = IntegerField("Port", validators=[DataRequired()])
    # mq_user = StringField("User", validators=[DataRequired()])
    # mq_password = PasswordField("Password", validators=[DataRequired()])
    # db_host = StringField("Hostname", validators=[DataRequired()])
    # db_port = IntegerField("Port", validators=[DataRequired()])
    # db_user = StringField("User", validators=[DataRequired()])
    # db_password = PasswordField("Password", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired(),
                                         URL(require_tld=False)])


class ServerForm(FlaskForm):
    hostname = StringField('Hostname *', validators=[DataRequired()])
    ip = StringField(
        'IP Address *', validators=[DataRequired(), IPAddress()])
    ldap_password = PasswordField(
        'LDAP Admin Password *', validators=[
            DataRequired(),
            validators.EqualTo('ldap_password_confirm',
                               message='Passwords must match')
        ])
    ldap_password_confirm = PasswordField(
        'Re-enter LDAP Admin Password *', validators=[DataRequired()])


class TestUser(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[
        DataRequired(), Email("Please enter valid email address.")])


class InstallServerForm(FlaskForm):
    hostname = StringField('Hostname *', validators=[DataRequired()])
    ip_address = StringField(
        'IP Address *', validators=[DataRequired(), IPAddress()])
    ldap_password = StringField(
        'LDAP Admin Password *', validators=[DataRequired()])
    countryCode = StringField(
        'Two Letter Country Code *', validators=[Length(min=2, max=2),
                                                 DataRequired()])
    state = StringField('Two Letter State Code *',
                        validators=[Length(min=2, max=2), DataRequired()])
    city = StringField('City *', validators=[DataRequired()])
    orgName = StringField('Organization Name *', validators=[DataRequired()])
    admin_email = StringField('Admin E-mail *', validators=[DataRequired()])
    inumOrg = StringField("inumOrg * (Please don't change this unless you know what you do)", validators=[DataRequired()])
    inumAppliance = StringField("inumAppliance * (Please don't change this unless you know what you do)", validators=[DataRequired()])

    installOxAuth = BooleanField('Install oxAuth', default=True)
    installOxTrust = BooleanField('Install oxTrust', default=True)
    installLDAP = BooleanField('Install LDAP', default=True)
    installHTTPD = BooleanField('Install Apache 2 web server', default=True)
    installJce = BooleanField('Install JCE 1.8')
    installSaml = BooleanField('Install Shibboleth SAML IDP')
    installAsimba = BooleanField('Install Asimba SAML Proxy')
    # installCas = BooleanField('Install CAS')
    installOxAuthRP = BooleanField('Install oxAuth RP')
    installPassport = BooleanField('Install Passport')

    ldap_type = RadioField(
        "Ldap Type",
        choices=[
            ("opendj", "OpenDJ",),
            # ("openldap", "OpenLDAP")
        ],
        validators=[AnyOf(["opendj", "openldap"])],
        default='opendj'
    )

    gluu_licence = SelectField(
        "Do you acknowledge that use of the Gluu Server is under the MIT license?",
        choices=[('no', "No"), ('yes', "Yes")]
    )
    oracle_licence = SelectField(
        "You must accept the Oracle Binary Code "
        "License Agreement for the Java SE Platform Products to "
        "download this software. Accept License Agreement?",
        choices=[('no', "No"), ('yes', "Yes")]
    )

    def validate_gluu_licence(form, field):
        if not field.data == 'yes':
            raise ValidationError("Can't proceed without accepting licence.")

    def validate_oracle_licence(form, field):
        if not field.data == 'yes':
            raise ValidationError("Can't proceed without accepting licence.")


def replace_pubkey_whitespace(value):
    if value is not None and hasattr(value, "replace"):
        return value.replace(" ", "")
    return value


class LicenseSettingsForm(FlaskForm):
    license_id = StringField("License ID", validators=[DataRequired()])
    license_password = StringField("License Password", validators=[DataRequired()])
    public_password = StringField("Public Password", validators=[DataRequired()])
    public_key = StringField("Public Key", validators=[DataRequired()],
                             filters=[replace_pubkey_whitespace])
    update = SubmitField("Update")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Login")


class LicenseAckForm(FlaskForm):
    accept = SubmitField("Accept")
    decline = SubmitField("Decline")


class FSReplicationPathsForm(FlaskForm):
    fs_paths = TextAreaField()
    update = SubmitField("Install File System Replication")


class LogSearchForm(FlaskForm):
    type = SelectField("Type", choices=[
        ("", ""),  # all types
        ("opendj", "OpenDJ"),
        ("oxauth", "oxAuth"),
        ("oxtrust", "oxTrust"),
        ("httpd", "HTTPD"),
        ("redis", "Redis"),
    ])
    message = StringField("Message")
    host = SelectField("Host", choices=[])
    search = SubmitField("Search")

class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[
                                DataRequired(),
                                    validators.EqualTo('passwordconfirm',
                               message='Passwords must match')
                ])
    passwordconfirm = PasswordField("Re-enter Password", validators=[DataRequired()])
    login = SubmitField("Sign up")
