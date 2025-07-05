
import json
import os
from datetime import datetime

class SystemDatabase:
    def __init__(self, db_file='systems_database.json'):
        self.db_file = db_file
        self.data = self.load_data()
    
    def load_data(self):
        """Carga la base de datos desde el archivo JSON"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return self.create_empty_database()
        return self.create_empty_database()
    
    def create_empty_database(self):
        """Crea una base de datos vacía"""
        return {
            'systems': {},
            'stats': {
                'total_systems': 0,
                'top_explorers': {}
            }
        }
    
    def save_data(self):
        """Guarda la base de datos al archivo JSON"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving database: {e}")
    
    def system_exists(self, system_name):
        """Verifica si un sistema ya existe"""
        return system_name.lower() in self.data['systems']
    
    def add_system(self, system_name, user_id, user_name, system_data):
        """Añade un nuevo sistema a la base de datos"""
        timestamp = datetime.now().isoformat()
        
        # Crear clave única para evitar colisiones
        base_key = system_name.lower()
        unique_key = base_key
        counter = 1
        
        # Si ya existe, agregar un sufijo numérico
        while unique_key in self.data['systems']:
            unique_key = f"{base_key}_{counter}"
            counter += 1
        
        # Añadir sistema con clave única
        self.data['systems'][unique_key] = {
            'original_name': system_name,
            'explorer_id': user_id,
            'explorer_name': user_name,
            'timestamp': timestamp,
            'system_data': system_data,
            'unique_key': unique_key
        }
        
        # Actualizar estadísticas
        self.data['stats']['total_systems'] += 1
        
        # Actualizar top explorers
        if str(user_id) not in self.data['stats']['top_explorers']:
            self.data['stats']['top_explorers'][str(user_id)] = {
                'name': user_name,
                'systems_explored': 0
            }
        
        self.data['stats']['top_explorers'][str(user_id)]['systems_explored'] += 1
        self.data['stats']['top_explorers'][str(user_id)]['name'] = user_name  # Update name in case it changed
        
        self.save_data()
    
    def get_system(self, system_name):
        """Obtiene información de un sistema específico - devuelve el más reciente si hay duplicados"""
        base_key = system_name.lower()
        
        # Buscar sistemas que coincidan con el nombre base
        matching_systems = []
        for key, system_data in self.data['systems'].items():
            if key == base_key or key.startswith(f"{base_key}_"):
                if system_data['original_name'].lower() == base_key:
                    matching_systems.append((key, system_data))
        
        if not matching_systems:
            return None
        
        # Devolver el sistema más reciente
        matching_systems.sort(key=lambda x: x[1]['timestamp'], reverse=True)
        return matching_systems[0][1]
    
    def get_top_explorers(self, limit=10):
        """Obtiene los mejores exploradores"""
        explorers = list(self.data['stats']['top_explorers'].items())
        explorers.sort(key=lambda x: x[1]['systems_explored'], reverse=True)
        return explorers[:limit]
    
    def get_total_systems(self):
        """Obtiene el número total de sistemas explorados"""
        return self.data['stats']['total_systems']
    
    def get_systems_by_explorer(self, user_id):
        """Obtiene todos los sistemas explorados por un usuario específico"""
        user_systems = []
        for system_data in self.data['systems'].values():
            if system_data['explorer_id'] == user_id:
                user_systems.append(system_data)
        return sorted(user_systems, key=lambda x: x['timestamp'], reverse=True)
