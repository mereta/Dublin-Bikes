try:
    # these imports work when running installed package.
    from .app import app
    from . import config
except:
    # these imports work when running locally on development machine.
    from app import app
    import config


def main():
    app.config.from_object(config.DevelopmentConfig)
    app.run()

if __name__ == "__main__":
    main()
