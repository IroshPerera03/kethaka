# 🎉 කේතක (Kethaka) 🎉

Welcome to කේතක (Kethaka), a Sinhala Java-like compile-time coding language! This project allows you to write code in Sinhala and compile it to Python bytecode for execution. 🚀

## 🛠️ Setup

Follow these steps to set up the කේතක project on your local machine:

1. **Clone the repository** 📂:
    ```sh
    git clone https://github.com/IroshPerera03/Kethaka.git
    cd kethaka
    ```

2. **Ensure Python is installed** 🐍:
    Make sure you have Python 3 installed on your system. You can check this by running:
    ```sh
    python3 --version
    ```

3. **Install required dependencies** 📦:
    ```sh
    pip install -r requirements.txt
    ```

4. **Make the scripts executable** 🔧:
    ```sh
    chmod +x kethaka kethakac
    ```

## 🚀 Available Commands

### Compile a Sinhala source file to bytecode

```sh
./kethakac <source_file.snl>
```

### Run the compiled bytecode

```sh
./kethaka <bytecode_file.kbc>
```

## 📚 Keyword Reference

This section provides a comparison between the custom Sinhala tokens used in the lexer and their respective Java equivalents.

| Sinhala Token | Description                  | Java Equivalent Token |
|---------------|------------------------------|-----------------------|
| `සඳහන්`      | Variable declaration         | `var`                 |
| `මුද්‍රණය`    | Print statement              | `print`               |
| `නම්`         | If condition                 | `if`                  |
| `නැතහොත්`    | Else condition               | `else`                |
| `දක්වා`       | For loop                     | `for`                 |
| `ක්‍රියාව`    | Function declaration         | `function`            |
| `ආපසු`       | Return statement             | `return`              |

## 🌟 Example

Here is a simple example of a Sinhala source file (`example.snl`):

```sinhala
සඳහන් x = 10;
මුද්‍රණය(x);
```

To compile and run this example:

1. Compile the source file to bytecode:
    ```sh
    ./kethakac example.snl
    ```

2. Run the compiled bytecode:
    ```sh
    ./kethaka example.kbc
    ```

## 🤝 Contributing

We welcome contributions to the කේතක project! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request. Your help is greatly appreciated! 🙌

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 💖 Acknowledgements

Special thanks to all the contributors and supporters of this project. Your efforts are greatly appreciated! 🌟
