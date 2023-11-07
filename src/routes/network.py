from flask import Blueprint, jsonify, request, abort
from paramiko import AuthenticationException, SSHException
from src.config.netmiko_config import cisco_device
from netmiko import ConnectHandler, NetMikoTimeoutException
from src.utils.network_template import template
from src.utils.ip_verif import ip_belongs_to_cidr

network_bp = Blueprint('network', __name__)


@network_bp.route('/test', methods=['GET'])
def test():
    try:
        # Intenta establecer una conexión SSH al dispositivo Cisco
        net_connect = ConnectHandler(**cisco_device)
        print("test")
        # Realiza una operación simple para verificar que Netmiko está funcionando
        prompt = net_connect.find_prompt()

        # Cierra la conexión
        net_connect.disconnect()

        return jsonify({'message': 'Netmiko está funcionando correctamente.'})

    except (NetMikoTimeoutException, SSHException, AuthenticationException) as e:
        return jsonify({'error': str(e)}), 500

@network_bp.route('/vlaninf', methods=['POST'])
def vlaninf():
    try:
        data = request.get_json()
        if 'mac' not in data:
            abort(400)
        mac = data['mac']
        # Iniciar la conexión SSH
        net_connect = ConnectHandler(**cisco_device)
        command_output = net_connect.send_command(
            f'show mac address-table address {mac}', use_textfsm=True)
        print(f'show mac address-table address {mac}')
        # Verificar si la respuesta contiene al menos una entrada válida de MAC
        print(command_output)
        if not command_output or not isinstance(command_output, list):
            print("No se encontro la mac")
            abort(404)

        tmp = command_output[0]['vlan']
        command_output2 = (net_connect.send_command(
            f'show ip interface vlan {tmp}', use_textfsm=True))[0]

        # Combinar todas las ipaddr y mask en un solo formato (ipaddr/mask)
        ipaddr_mask_list = []
        for ip, mask in zip(command_output2['ipaddr'], command_output2['mask']):
            ipaddr_mask_list.append(f"{ip}/{mask}")

        # Modificar el objeto para incluir la lista de ipaddr/mask
        command_output2['cidr'] = ipaddr_mask_list
        return jsonify({"vlan": command_output2['intf'], "segments": ipaddr_mask_list})
    except Exception as e:
        print(str(e))
        # return jsonify({'error': str(e)})
        abort(404)
        
        
        
        
@network_bp.route('/check_ip', methods=['POST'])
def check_ip():
    try:
        data = request.get_json()
        if 'ip' not in data or 'cidr' not in data:
            return jsonify({'error': 'Se requiere una dirección IP y un CIDR en el JSON.'}), 400

        ip = data['ip']
        cidr = data['cidr']

        if ip_belongs_to_cidr(ip, cidr):
            return jsonify({'status': True})
        else:
            return jsonify({'status': False})
    except Exception as e:
        return jsonify({'error': str(e)}), 404
    
    
@network_bp.route('/test2', methods=['GET'])
def test2():
    try:
        # Intenta establecer una conexión SSH al dispositivo Cisco
        net_connect = ConnectHandler(**cisco_device)
        
        # Ejecuta un comando para obtener todas las MAC addresses de la VLAN 1
        mac_addresses = net_connect.send_command(
            'show mac address-table vlan 1', use_textfsm=True)
        
        # Cierra la conexión
        net_connect.disconnect()

        # Extrae las MAC addresses y las devuelve como respuesta JSON
        mac_list = [entry['destination_address'] for entry in mac_addresses]
        
        return jsonify({'mac_addresses': mac_list})

    except (NetMikoTimeoutException, SSHException, AuthenticationException) as e:
        return jsonify({'error': str(e)}), 500