from subprocess import check_output, CalledProcessError


def get_clamav():
    try:
        return check_output('which clamscan', shell=True).decode('utf-8')
    except:
        return


def scan(path):
    clamav_path = get_clamav()
    if clamav_path:
        try:
            check_output([
                'clamscan', path,
                '--no-summary', '--recursive=yes', '--infected'
            ]).decode('utf-8')
        except CalledProcessError as e:
            output = e.output.decode('utf-8').split('\n')[:-1]
            print(output)
            infected_list = []
            for l in output:
                file, status_raw = l.rsplit(': ', 1)
                virus_type, status = status_raw.rsplit(' ', 1)
                infected_list.append((file, virus_type, status))
            return infected_list
    else:
        raise Exception('** CLAMAV NOT FOUND. **')


if __name__ == '__main__':
    a = scan('/home/kenobi/Desktop')
    print(a)
