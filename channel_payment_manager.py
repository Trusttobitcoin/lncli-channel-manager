import subprocess
import json

def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def get_channels():
    output = run_command("lncli listchannels")
    return json.loads(output)

def find_channel_with_largest_outbound_capacity(channels):
    max_outbound_capacity = 0
    selected_channel = None
    for channel in channels['channels']:
        local_balance = int(channel['local_balance'])
        if local_balance > max_outbound_capacity:
            max_outbound_capacity = local_balance
            selected_channel = channel
    return selected_channel

def pay_invoice(invoice, channel_id):
    command = f"lncli payinvoice --force --outgoing_chan_id={channel_id} '{invoice}'"
    output = run_command(command)
    return output

# Main flow
channels_info = get_channels()
channel = find_channel_with_largest_outbound_capacity(channels_info)

if channel:
    # Get invoice from user
    user_invoice = input("Please enter the invoice to pay: ")
    print(f"Paying through channel ID: {channel['chan_id']} with outbound capacity: {channel['local_balance']}")
    pay_result = pay_invoice(user_invoice, channel['chan_id'])
    print(pay_result)
else:
    print("No channel with sufficient outbound capacity found.")
