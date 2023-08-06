# Workshop toolchain CLI
## ⚙️ Requirements

 -  [Node.js](https://nodejs.org/)<sup>1</sup>
 -  [Java](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)<sup>2</sup>
 -  [GCC]( https://gcc.gnu.org/install/binaries.html)<sup>3</sup>

<sup>1</sup>required to validate JavaScript exercises  
<sup>2</sup>required to validate Java exercises  
<sup>3</sup>required to validate C exercises  

## 🛠️ Installation
Please follow the system-specific instructions:
- [Windows](install_instructions/win.md)
- [OsX/macOS](install_instructions/osx.md)
- [Linux](install_instructions/linux.md)

## 📚 Available commands

| Command                    | Description                                      |
| -------------------------- | ------------------------------------------------ |
| `gf config`                | Configure the application.                       |
| `gf start <workshop_name>` | Start the daily workshop with downloading        |
| `gf open`                  | Open the downloaded workshop                     |
| `gf rate <filename>`       | Rate the selected exercise.                      |
| `gf verify <filename>`     | Verify the selected exercise.                    |
| `gf lint <filename>`       | Detect stylistic errors.                         |
| `gf -v ` or`gf --version`  | Display the actual version of workshop toolchain.|

## 📄 Usage

#### AFTER THE INSTALLATION: 
**1.** You have to execute `gf config` and provide your GitHub credentials.
Choose your language **WITHOUT** using quote. Then write `y`, if you are in the
correct directory. 
It will create a GitHub token and store it under `.gf/` folder **in**
your home directory.

##### !FOR WINDOWS USERS!
Users should execute `gf config` either in windows CMD **OR** 
should execute `winpty gf config`.

**2.** Then you will have to initialize the day by executing `gf start <workshop_name>`.
It will download the exercises for that day into the current directory. 
**One folder represents one day** so you can only use this command 
**ONCE** in a folder. 
*Workshop_name* is the name to the current workshop's language specified markdown file.

**3.** After you have downloaded your daily workshop you should execute 
`gf open` to open the actual workshop in a new browser tab. 

**4.** Before you verify the selected exercise, please execute `gf lint <filename>` to check 
the clean code.

**5.** When you have *the solution* for an exercise you can verify it by the 
`gf verify <filename>` command.

**6.** You can rate an exercise between `1` to `5` by the `gf rate <filename>` command.

