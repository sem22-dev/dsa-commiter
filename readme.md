# DSA Commiter CLI 🚀

A lightweight command-line tool to create directories and files for your DSA (Data Structures & Algorithms) solutions and automatically commit and push them to GitHub. Perfect for tracking LeetCode progress.

---

## 📌 Why I Built This

I created this CLI to streamline committing and pushing my LeetCode solutions, helping me stay organized and consistent with my DSA practice.

---

## ✨ Features

* 📁 Create directories and files with default code templates (e.g., .py, .js, .cpp)
* ✍️ Add multiline content (e.g., LeetCode solutions) with Ctrl+D or two blank lines to finish
* 🔄 Automatically git add, commit, and push to your current branch (main or master)
* 🎨 Clean, colorful terminal interface using [rich](https://github.com/Textualize/rich)
* 🛡️ Robust error handling for file creation and Git operations

---

## 🚀 Quick Start

Clone the repository:

```bash
git clone https://github.com/sem22-dev/dsa-commiter.git
cd dsa-commiter
```

---

## 💻 Installation

### 🌐 macOS / Linux

Run the installation script:

```bash
chmod +x install.sh
./install.sh
```

### 📺 Windows

Run the batch installer:

```cmd
install.bat
```

Make sure you have **Python**, **pip**, and **Git** in your system PATH.

---

## 💻 Usage

Navigate to a project directory linked with a remote repository. Then run:

```bash
dsa-commiter
```

Follow the prompts to:

* 📂 Enter a directory name (or press Enter for current directory)
* 📄 Enter a file name (e.g., solution.py)
* ✍️ Enter file content (e.g., a LeetCode solution), ending with Ctrl+D or two blank lines
* 🔄 The CLI auto-commits and pushes to your current branch

Example:

```
📁 Enter directory name (or press Enter): problems
📝 Supported file extensions: .py, .js, .cpp, .java, .c, .txt
📄 Enter file name (e.g., solution.py): solution.py
📝 Enter file content (Ctrl+D or two blank lines to end):
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
[Ctrl+D]

📅 Created directory: /path/to/problems
📅 Created file: /path/to/problems/solution.py
🔢 Added file: problems/solution.py
📅 Committed with message: 'problems/solution.py solution'
🛁 Pushed file: problems/solution.py to branch 'master'
```

---

If `dsa-commiter` is not recognized, use:

```cmd
venv\Scripts\activate
python -m dsa_commiter.cli_interface
```

---

## 📁 Project Structure

```
dsa-commiter/
├── dsa_commiter/
│   ├── __init__.py
│   ├── cli_interface.py
│   ├── file_operations.py
│   ├── git_operations.py
├── install.sh
├── install.bat
├── setup.py
├── README.md
```

---

## 📜 Requirements

* Python 3.7+
* Git
* `rich` library (installed via script)

---

## 📄 License

MIT License

---

**Happy Coding! 🎉**
