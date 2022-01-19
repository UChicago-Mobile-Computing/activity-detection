# Lab 1: Activity Detection

Starter code for Lab 1 in [CMSC 23400: Mobile Computing](https://people.cs.uchicago.edu/~htzheng/teach/cs23400/) (University of Chicago, 2022)

## Setup

1. Download this repository onto your computer by going to `Code > Download ZIP` on the top-right of the GitHub page or by running `git clone git@github.com:UChicago-Mobile-Computing/activity-detection.git` with [git installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
2. Install Python 3.6 or above. This may be preinstalled on your system (run `python3` on the command line to check), or [download the latest version](https://www.python.org/downloads/).
3. Install required packages: `pip3 install -r requirements.txt`
4. Download the [train/test dataset](https://drive.google.com/file/d/14SCF6hTgnQTu5ZHddTghG3lewVoCiyM0/view?usp=sharing) and unzip it such that `data/train` and `data/test_unlabeled` are subdirectories of this repository.

**Optional GitHub Setup**

If you would like to collaborate with your team using [GitHub](https://github.com/), follow these steps to upload the starter code to your own repository:

1. Ensure you've downloaded this repository through the `git clone` method above, *not* by downloading the ZIP.
2. Click the "+" icon at the top on GitHub, then select **Create new repository**.
3. Name your repository, and mark it as **private**. **Note that work done in public repositories of this lab may not earn credit.**
4. Click **create repository**.
5. Navigate to this repository on your computer through the command line, then follow the instructions for "pushing an existing repository from the command line." Use your GitHub username in place of `$USERNAME` and your repository name in place of `$REPO_NAME` below:

```
git remote rename origin upstream
git remote add origin git@github.com:$USERNAME/$REPO_NAME.git
git branch -M main
git push -u origin main
```

## Assignment & submission requirements

Please refer to [this document](https://docs.google.com/document/d/1HKSX5XHLAX8O8e_MBuM2guvQD2PaT-Z-W65o4g5yApo/edit) for the latest assignment instructions. Submissions are **due via Gradescope by Thursday, February 3 at 11:59pm CT**.