class Process:
    def display_nas_data(volume_data):
        total_volume = 0
        used_volume = 0
        for volume in volume_data:
            total_volume += int(volume['size']['total'])
            used_volume += int(volume['size']['used'])

        percentage_used = (used_volume / total_volume) * 100

        return f"{Process._format_bytes(used_volume)} / {Process._format_bytes(total_volume)} ({percentage_used:.0f}%)"

    def display_block_data(block_data):
        return [
            f"Block {block_data['ads_blocked_today']}/{block_data['dns_queries_today']}",
            f"{block_data['ads_percentage_today']}% blocked"
        ]
    
    def display_prometheus_details(cpu_alloc, ram_alloc, cpu_temp):
        cpu = '{:.0f}'.format(float(cpu_alloc[0]['value'][1]))
        ram = '{:.0f}'.format(float(ram_alloc[0]['value'][1]))
        tmp = '{:.0f}'.format(float(cpu_temp[0]['value'][1]))
        return f"C: {cpu}% R: {ram}% T: {tmp}C";

    def _format_bytes(num):
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        i = 0

        while num >= 1024 and i < len(units)-1:
            num /= 1024
            i += 1

        formatted_num = '{:.2f}'.format(num)

        result = f"{formatted_num} {units[i]}"

        return result
