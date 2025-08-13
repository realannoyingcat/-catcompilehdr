import os
import sys
import subprocess

def generate_c_code(folder_path):
    folder_path_escaped = folder_path.replace("\\", "\\\\")
    return f"""#include <Python.h>

int main() {{
    Py_Initialize();
    PyRun_SimpleString(
        "import os\\n"
        "import sys\\n"
        "from tkinter import *\\n\\n"
        "sys.path.insert(0, '{folder_path_escaped}')\\n\\n"
        "root = Tk()\\n"
        "root.title('wawa ap i')\\n"
        "root.geometry('600x400')\\n\\n"
        "for file in os.listdir('{folder_path_escaped}'):\\n"
        "    if file.endswith('.py'):\\n"
        "        module = file[:-3]\\n"
        "        try:\\n"
        "            __import__(module)\\n"
        "            if hasattr(sys.modules[module], 'main'):\\n"
        "                sys.modules[module].main(root)\\n"
        "        except Exception as e:\\n"
        "            print(f'Failed to load {{module}}: {{e}}')\\n\\n"
        "root.mainloop()"
    );
    Py_Finalize();
    return 0;
}}"""

def compile_project(prompt):
    try:
        folder_name = prompt.replace(" ", "_").lower()
        os.makedirs(folder_name, exist_ok=True)
        
        # Generate C code
        c_code = generate_c_code(os.path.abspath(folder_name))
        c_file_path = os.path.join(folder_name, "wawa_gui.c")
        with open(c_file_path, "w") as f:
            f.write(c_code)
        
        # Output executable name
        output_exe = os.path.join(folder_name, "wawa")
        if os.name == "nt":
            output_exe += ".exe"
        
        # Get Python dev paths
        python_include = subprocess.getoutput(f"{sys.executable} -c \"import sysconfig; print(sysconfig.get_paths()['include'])\"")
        python_lib = subprocess.getoutput(f"{sys.executable} -c \"import sysconfig; print(sysconfig.get_config_var('LIBDIR'))\"")
        python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
        
        # Compile command
        compile_cmd = [
            "gcc",
            c_file_path,
            "-o", output_exe,
            f"-I{python_include}",
            f"-L{python_lib}",
            f"-l{python_version}"
        ]
        
        subprocess.run(compile_cmd, check=True)
        print(f"\n✅ Success! Compiled to: {output_exe}")
        
    except Exception as e:
        print(f"\n❌ Compilation failed: {str(e)}")

def main():
    print("🐾 WAWA C Compiler (Midjourney-style)")
    print("Type '--help' for usage instructions")
    
    while True:
        try:
            prompt = input("\nWAWA> ")
            if prompt.lower() == "--help":
                print("\nHOW TO USE:")
                print("1. Enter a folder name when prompted")
                print("2. Place your Python files in the created folder")
                print("3. Each file should contain a 'main(root)' function")
                print("4. Re-run the compiler to rebuild")
                print("5. Run the output executable")
            elif prompt:
                compile_project(prompt)
        except KeyboardInterrupt:
            print("\nExiting compiler...")
            sys.exit(0)

if __name__ == "__main__":
    main()
