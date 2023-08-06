import os

from .utils import exec_cmd


def generate_jks(passwd, javalibs_dir, jks_path, exp=365,
                 alg="RS256 RS384 RS512 ES256 ES384 ES512"):
    if os.path.exists(jks_path):
        os.unlink(jks_path)

    cmd = " ".join([
        "java",
        "-jar", os.path.join(javalibs_dir, "keygen.jar"),
        "-algorithms", alg,
        "-dnname", "{!r}".format("CN=oxAuth CA Certificates"),
        "-expiration", "{}".format(exp),
        "-keystore", jks_path,
        "-keypasswd", passwd,
    ])
    return exec_cmd(cmd)
