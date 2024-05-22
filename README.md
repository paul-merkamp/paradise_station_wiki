## overview

This is a simple set of tools meant to aid with editing the [Paradise Station Wiki](https://paradisestation.org/wiki/index.php?title=Main_Page).

## credentials

DISCLAIMER: This is not a secure method of storing credentials. I only did it this way because I'm lazy. Anyone who can access your environment variables can see your password.

```
export MW_USERNAME=yourusernamehere
export MW_PASSWORD=yourpasswordhere
```

## dependencies

Install with

```bash
python3 -m pip install mwclient termcolor
```

## download.py

This script will attempt to download every wiki page into a `wiki` directory. It will update any outdated pages.

Usage:

```bash
python3 download.py [downloadAttachments={true, false}]
```

## upload.py

This script will attempt to upload a provided wiki page. First, it shows the diff and asks the user to confirm. Then, it asks for a commit message. Finally, it pushes the page.

Usage:

```bash
python3 upload.py wiki/[file.wiki]
```
