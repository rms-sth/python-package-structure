from invoke import task


@task
def docs_github_pages(ctx):
    """publishes to gh-pages in github.io"""

    gh_branch = ctx.run("git branch --all")
    gh_branch = str(gh_branch.stdout)
    if "gh-pages" not in gh_branch:
        ctx.run("mkdocs gh-deploy --force")
    else:
        latest_tag = ctx.run("git tag -l --sort=-creatordate | head -n 1")
        latest_tag = str(latest_tag.stdout).strip()
        git_cmd = """
                git config --local user.email "github-actions[bot]@users.noreply.github.com"
                git config --local user.name "github-actions[bot]"
                git branch -D gh-pages
                git checkout gh-pages
                git pull --rebase
                git checkout master
        """
        ctx.run(git_cmd)
        mike_deploy_cmd = f"mike deploy --push --update-aliases {latest_tag} latest"
        ctx.run(mike_deploy_cmd)
        ctx.run("mike set-default --push latest")
