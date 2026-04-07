class PlayerStats:
    def __init__(self):
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.max_stamina = 100
        self.current_stamina = self.max_stamina
        self.max_shield = self.max_hp
        self.current_shield = 0
        
        self.armor = 0
        
        self.score = 0
        self.default_speed = 400
        self.speed = self.default_speed
        
        self.basic_inventory_capacity = 40
        
        # Stamina rates (points per second)
        self.stamina_depletion_rate = 100
        self.stamina_regen_rate = 50
        self.stamina_accumulator = 0  
        
        
        
    
        