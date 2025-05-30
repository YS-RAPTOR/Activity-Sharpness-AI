# How to Run

## Preparations

- Clone the project and open the directory.

```bash
git clone https://github.com/YS-RAPTOR/COS40007.git
cd COS40007
```

- Install [uv](https://docs.astral.sh/uv/getting-started/installation/), [node](https://nodejs.org/en/download) and [pnpm](https://pnpm.io/installation).
- Download the [folder](https://liveswinburneeduau-my.sharepoint.com/:f:/g/personal/102838834_student_swin_edu_au/EnoGDAtkr0VGhiQt4whRIokBpXRMTgVa1dtEWviIOPwfLA?e=oaaTEq) linked and extract the folder's content to the models folder. The directory structure after this operation should look like structure below.
```bash
.
|— models
|   |— Models_Knife Sharpness
|   |   |— ...
|   |— Models_Activity
|   |   |— ...
|   |— ...
|— ...
```

## Server

The following command will start the server:
```bash
uv run fastapi run ./server/main.py
```

## GUI
The following commands will start the GUI:

```bash
cd gui
pnpm install .
pnpm run dev
```
