# InstagramUnfollower

---

Unfollow the people who don't follow you back on Instagram

## Prerequisites:

- [Python](https://www.python.org/downloads/)
- [Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/)

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
TWO_FACTOR=False
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

```bash
python unfollowList.py
```

This will unfollow the users in `people_to_unfollow.txt`. It might take a while, so be patient. 

---

