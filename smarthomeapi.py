from flask import Flask, request

app = Flask(__name__)

houses = []
floors = []
rooms = []

# House methods
def CreateHouse(house):
    for h in houses:
        if h['id'] == house['id']:
            return None
    house['floor_ids'] = []
    houses.append(house)
    return house

def GetHouseData(id):
    for house in houses:
        if house['id'] == id:
            return house
    return None

def UpdateHouse(id, house_info):
    for house in houses:
        if house['id'] == id:
            house['name'] = house_info['name']
            house['address'] = house_info['address']
            return house
    return None

def DeleteHouse(id):
    for house in houses:
        if house['id'] == id:
            for floor_id in house['floor_ids']:
                DeleteFloor(id, floor_id)
            houses.remove(house)
            return house
    return None

# Floor methods
def CreateFloor(house_id, floor):
    for f in floors:
        if f['id'] == floor['id']:
            return None
    floor['room_ids'] = []
    floors.append(floor)
    for house in houses:
        if house['id'] == house_id:
            house['floor_ids'].append(floor['id'])
            return floor
    return None

def GetFloor(floor_id):
    for floor in floors:
        if floor['id'] == floor_id:
            return floor

def UpdateFloor(floor_id, floor_info):
    for floor in floors:
        if floor['id'] == floor_id:
            floor['name'] = floor_info['name']
            return floor
    return None

def DeleteFloor(house_id, floor_id):
    for floor in floors:
        if floor['id'] == floor_id:
            for room_id in floor["room_ids"]:
                DeleteRoom(floor_id, room_id)
            floors.remove(floor)
            for house in houses:
                if house['id'] == house_id:
                    house['floor_ids'].remove(floor['id'])
                    return floor
    return None

# Room methods
def CreateRoom(floor_id, room):
    for r in rooms:
        if r['id'] == room['id']:
            return None
    rooms.append(room)
    for floor in floors:
        if floor['id'] == floor_id:
            floor['room_ids'].append(room['id'])
            return room
    return None

def GetRoom(room_id):
    for room in rooms:
        if room['id'] == room_id:
            return room
    return None

def UpdateRoom(room_id, room_info):
    for room in rooms:
        if room['id'] == room_id:
            room['name'] = room_info['name']
            return room
    return None

def DeleteRoom(floor_id, room_id):
    for room in rooms:
        if room['id'] == room_id:
            rooms.remove(room)
            for floor in floors:
                if floor['id'] == floor_id:
                    floor['room_ids'].remove(room['id'])
                    return room
    return None

# Endpoints
@app.route('/houses', methods=['POST'])
def create_house():
    house_info = request.get_json()
    house = CreateHouse(house_info)
    if not house:
        return 'House already exists\n', 404
    return f"House created: {house}\n", 201

@app.route('/houses/<int:id>', methods=['GET'])
def get_house(id):
    house = GetHouseData(id)
    if not house:
        return 'House not found\n', 404
    return f"House found: {house}\n", 200

@app.route('/houses/<int:id>', methods=['PUT'])
def update_house(id):
    house_info = request.get_json()
    house = UpdateHouse(id, house_info)
    if not house:
        return 'House not found\n', 404
    return f"House updated: {house}\n", 200

@app.route('/houses/<int:id>', methods=['DELETE'])
def delete_house(id):
    house = DeleteHouse(id)
    if not house:
        return 'House not found\n', 404
    return 'House deleted successfully\n', 200

@app.route('/houses/<int:house_id>/floors', methods=['POST'])
def create_floor(house_id):
    floor_info = request.get_json()
    floor = CreateFloor(house_id, floor_info)
    if not floor:
        return 'House not found or floor already exists\n', 404
    return f"Floor created: {floor}\n", 201

@app.route('/floors/<int:floor_id>', methods=['GET'])
def get_floor(floor_id):
    floor = GetFloor(floor_id)
    if not floor:
        return 'Floor not found\n', 404
    return f"Floor found: {floor}\n", 200

@app.route('/floors/<int:floor_id>', methods=['PUT'])
def update_floor(floor_id):
    floor_info = request.get_json()
    floor = UpdateFloor(floor_id, floor_info)
    if not floor:
        return 'Floor not found\n', 404
    return f"Floor updated: {floor}\n", 200

@app.route('/houses/<int:house_id>/floors/<int:floor_id>', methods=['DELETE'])
def delete_floor(house_id, floor_id):
    floor = DeleteFloor(house_id, floor_id)
    if not floor:
        return 'Floor not found\n', 404
    return 'Floor deleted successfully\n', 200

@app.route('/floors/<int:floor_id>/rooms', methods=['POST'])
def create_room(floor_id):
    room_info = request.get_json()
    room = CreateRoom(floor_id, room_info)
    if not room:
        return 'Room already exists or floor not found\n', 400
    return f"Room created: {room}\n", 201

@app.route('/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    room = GetRoom(room_id)
    if not room:
        return 'Room not found\n', 404
    return f"Room found: {room}\n", 200

@app.route('/rooms/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    room_info = request.get_json()
    room = UpdateRoom(room_id, room_info)
    if not room:
        return 'Room not found\n', 404
    return f"Room updated: {room}\n", 200

@app.route('/floors/<int:floor_id>/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(floor_id, room_id):
    room = DeleteRoom(floor_id, room_id)
    if not room:
        return 'Room not found\n', 404
    return 'Room deleted successfully\n', 200

if __name__ == '__main__':
    app.run(debug=True)
