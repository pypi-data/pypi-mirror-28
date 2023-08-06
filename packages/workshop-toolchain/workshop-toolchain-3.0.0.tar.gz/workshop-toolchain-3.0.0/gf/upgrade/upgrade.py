import pip


def upgrade_the_old_module():
    try:
        pip.main(["install", "--upgrade", "workshop-toolchain"])
    except SystemExit as e:
        pass
