import os,codecs,json


def main(file1, file2, new_file):
    results = []
    with open(file1, 'r') as f:
        file1_lines = f.readlines()
    with open(file2, 'r') as f:
        file2_lines = f.readlines()

    count = 0
    new_name = 0
    for i in range(6525):
        if file1_lines[i] != "\n":
            results.append(file1_lines[i])
        else:
            count += 1
            if file2_lines[i] != "\n":
                new_name += 1
            results.append(file2_lines[i])
    print (count)
    print (new_name)
    # with open(new_file, 'w') as f:
    #     for name in results[:-1]:
    #         f.write(name)
    #     f.write(results[-1])


if __name__ == '__main__':
    main('../data/names.txt', '../data/names_secondary.txt', '../data/new_names.txt')