# InstagramUnfollower

---

Unfollow the people who don't follow you back on Instagram

## Prerequisites:

- [Python](https://www.python.org/downloads/)
- [Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/)
- [Google Chrome](https://support.google.com/chrome/answer/95346?hl=en&co=GENIE.Platform%3DDesktop)

## How to use

**1. Clone Repository**

Running these lines in the terminal will clone the repository, create and activate a new conda environment, and install the program's dependencies.

```bash
git clone https://github.com/roest1/InstagramUnfollower.git

cd InstagramUnfollower

conda create --name igUnfollower

conda activate igUnfollower

pip install -r requirements.txt
```

**2. Setup Login Credentials**

Run this line in your terminal

```bash
cp .env.sample .env
```

And fill the .env file with your credentials.

Example:

```env
IG_USERNAME=username
IG_PASSWORD=password
USERNAMES_FILENAME=people_to_unfollow
```

Note that the `USERNAMES_FILENAME` is automatically set to `people_to_unfollow.txt`. The program will automatically include the `.txt` extension when referencing this file. 

`people_to_unfollow.txt` is automatically generated after running `getList.py`.

Make sure to save the .env file after editing.

**3. Run `getList.py`**

```bash
python getList.py
```

This will generate a list of people who don't follow you back in `people_to_unfollow.txt`.

Go through the list and remove any users you don't want to unfollow before proceeding to the next step.

**4. Run `unfollowList.py`**

To see the script in action, run this command:

```bash
python unfollow_txt_file.py
```

Or have the script run in the background:

```bash
python unfollow_txt_file.py --headless
```

This will unfollow the users in `people_to_unfollow.txt`. It might take a while.

**5. Go through `errors.txt`**

It is likely some accounts weren't able to be unfollowed by the script for whatever reason. 

You can try going back to your `.env` file and setting the `USERNAMES_FILENAME` to `errors`, saving, and then run the `unfollowList.py` program again to try unfollowing these users again. 

Otherwise, you might just have to go and unfollow these people manually. ( \\_("/)_/ )

---

