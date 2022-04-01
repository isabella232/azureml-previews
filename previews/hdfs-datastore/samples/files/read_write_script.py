import argparse
import os

def test_read(dataset_path):
    for root, dirs, files in os.walk(dataset_path):
        for filename in files:
            print()
            print('=' * 32)
            print(os.path.join(root, filename))
            print('=' * 32)
            with open(os.path.join(root, filename), 'r') as f:
                for line in f:
                    print(line)

        for dirname in dirs:
            test_read(os.path.join(dirname))


def test_write(dataset_path):
    with open(os.path.join(dataset_path, 'helloworld.txt'), 'w') as f:
        f.writelines(['Hello World!'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--read-path', help = 'Path to input dataset')
    parser.add_argument('--write-path', help = 'Path to output dataset')
    args = parser.parse_args()

    if args.read_path:
        print(f'Recursively exploring {args.read_path}...')
        test_read(args.read_path)
    
    if args.write_path:
        print(f'Testing writes to {args.write_path}...')
        test_write(args.write_path)
