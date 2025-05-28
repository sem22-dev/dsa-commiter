# DSA Commiter CLI 🚀

A simple and handy command-line tool to manage and push your DSA (Data Structures & Algorithms) solutions to GitHub — perfect for tracking your LeetCode progress.

---

## 📌 Why I Built This

I created this tool to quickly commit and push my DSA solutions as I solve them. It helps me keep track of my [LeetCode](https://leetcode.com/) progress and stay consistent with my learning.

---

## ✨ Features

* 📁 Create folders and files with built-in code templates
* 🔄 Add, commit, and push to Git in a few steps
* 📂 View directory contents in a clean layout
* 🎨 Rich and colorful terminal interface using [`rich`](https://github.com/Textualize/rich)

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/yourusername/dsa-commiter.git
cd dsa-commiter

# Run the installation script
chmod +x install.sh
./install.sh
```

---

## 💻 Usage

Navigate to the local repository or project folder. Make sure it's already initialized with Git and connected to a remote repository.

Then run:

```bash
dsa-commiter
```

From there, follow the interactive prompts to:

1. 📂 Create directories and files
2. 🔄 Add, commit, and push your changes
3. 📃 List directory contents
4. ❌ Exit the tool

---

## 📁 Project Structure

```
dsa-commiter/
├── dsa_commiter/
│   ├── cli_interface.py
│   ├── file_operations.py
│   └── git_operations.py
├── install.sh
├── requirements.txt
├── setup.py
└── README.md
```

---

## 📆 Requirements

* Python 3.7+
* Git
* pip3

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

**Happy Coding! 🎉**
