from github import Github
from config import Config
from runner import Runner


def main():
    c = Config()
    g = Github(c.token)
    r = Runner(c, g)
    r.run()


if __name__ == "__main__":
    main()
