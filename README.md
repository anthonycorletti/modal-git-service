# modal-git-service

Host your own git service on [Modal](modal.com) with stateless RPC. It's like GitHub... with more cowbell.

> [!WARNING]
> This is meant for demo and learning purposes. Do not use this in production. 

This project uses `uv` to install and manage dependencies, so make sure you have `uv` installed.

## Try it out

Clone this repo and deploy to modal like so:

```
git clone https://github.com/anthonycorletti/modal-git-service.git && cd modal-git-service
bin/install
bin/deploy-modal
```

Grab the url of your deployed service. It should be something like `https://profilename--git-on-modal.modal.run`.

If you created at repo at `owner/repo`, run the following:

```
git clone https://casadotdev--git-on-modal.modal.run/owner/repo.git
```

There you have it! Your own little git service.
