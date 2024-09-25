# modal-git-service

Host your own git service on [Modal](modal.com) with stateless RPC. It's like GitHub... with more cowbell.

> [!WARNING]
> This is meant for demo and learning purposes. Do not use this in production. 

This project uses `uv` to install and manage dependencies, so make sure you have `uv` installed.

## Try it out

Clone this repo and deploy to modal like so:

```sh
git clone https://github.com/anthonycorletti/modal-git-service.git && cd modal-git-service
bin/install
bin/deploy-modal
```

Grab the url of your deployed service. It should be something like `https://PROFILENAME--git-on-modal.modal.run`.

Push some code to your service

```sh
mkdir repo && cd repo
echo "# hello world" > README.md
git init
git add -A
git commit -m "initial commit"
git remote add origin https://PROFILENAME--git-on-modal.modal.run/owner/repo.git
git push -u origin main
```

And clone it down
```sh
git clone https://PROFILENAME--git-on-modal.modal.run/owner/repo.git repo-clone
```

There you have it! Your own little git service.
