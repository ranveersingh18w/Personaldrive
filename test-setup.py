"""
Test script to verify Personal Cloud Storage setup
"""
import sys
import os
import importlib.util

def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Please upgrade to Python 3.7+")
        return False

def check_module(module_name, package_name=None):
    """Check if a Python module is installed"""
    if package_name is None:
        package_name = module_name
    
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name} - Installed")
        return True
    except ImportError:
        print(f"❌ {package_name} - Not installed")
        return False

def check_backend():
    """Check backend dependencies"""
    print("\n" + "="*50)
    print("Backend Dependencies")
    print("="*50)
    
    modules = [
        ('flask', 'Flask'),
        ('flask_cors', 'Flask-CORS'),
        ('PIL', 'Pillow'),
        ('werkzeug', 'Werkzeug')
    ]
    
    results = []
    for module, name in modules:
        results.append(check_module(module, name))
    
    return all(results)

def check_client():
    """Check client dependencies"""
    print("\n" + "="*50)
    print("Client Dependencies")
    print("="*50)
    
    modules = [
        ('requests', 'requests'),
        ('watchdog', 'watchdog')
    ]
    
    results = []
    for module, name in modules:
        results.append(check_module(module, name))
    
    return all(results)

def check_node():
    """Check if Node.js is installed"""
    print("\n" + "="*50)
    print("Frontend Requirements")
    print("="*50)
    
    try:
        import subprocess
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} - OK")
            return True
        else:
            print("❌ Node.js - Not found")
            return False
    except:
        print("❌ Node.js - Not found")
        return False

def check_npm():
    """Check if npm is installed"""
    try:
        import subprocess
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ npm {version} - OK")
            return True
        else:
            print("❌ npm - Not found")
            return False
    except:
        print("❌ npm - Not found")
        return False

def check_storage_folder():
    """Check if default storage folder is accessible"""
    print("\n" + "="*50)
    print("Storage Configuration")
    print("="*50)
    
    default_path = os.path.join(os.path.expanduser('~'), 'MyCloud', 'Photos')
    
    try:
        os.makedirs(default_path, exist_ok=True)
        print(f"✅ Storage folder accessible: {default_path}")
        return True
    except:
        print(f"❌ Cannot create storage folder: {default_path}")
        return False

def main():
    print("="*50)
    print("Personal Cloud Storage - System Check")
    print("="*50)
    
    results = []
    
    # Check Python
    results.append(check_python_version())
    
    # Check backend
    backend_ok = check_backend()
    results.append(backend_ok)
    
    if not backend_ok:
        print("\n💡 To install backend dependencies:")
        print("   cd backend")
        print("   pip install -r requirements.txt")
    
    # Check client
    client_ok = check_client()
    results.append(client_ok)
    
    if not client_ok:
        print("\n💡 To install client dependencies:")
        print("   cd client")
        print("   pip install -r requirements.txt")
    
    # Check Node.js and npm
    node_ok = check_node()
    npm_ok = check_npm()
    results.append(node_ok and npm_ok)
    
    if not (node_ok and npm_ok):
        print("\n💡 To install Node.js:")
        print("   Download from https://nodejs.org/")
    
    # Check storage
    results.append(check_storage_folder())
    
    # Final summary
    print("\n" + "="*50)
    print("Summary")
    print("="*50)
    
    if all(results):
        print("✅ All checks passed! You're ready to go.")
        print("\nNext steps:")
        print("1. Run setup.bat to install all dependencies")
        print("2. Run start-all.bat to start all services")
        print("3. Open http://localhost:3000 in your browser")
    else:
        print("⚠️  Some checks failed. Please install missing dependencies.")
        print("\nQuick fix:")
        print("   python -m pip install --upgrade pip")
        print("   Run setup.bat to install all dependencies")
    
    print("\n" + "="*50)

if __name__ == '__main__':
    main()
    input("\nPress Enter to exit...")
