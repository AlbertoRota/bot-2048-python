import pyximport;
pyximport.install()

import helloworld

def main():
    helloworld.say_hello_to("Alberto Rota")

if __name__ == '__main__':
    main()
