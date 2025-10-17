# src/domain/customer.py
# Entidad Customer - Lógica de negocio pura
# ==========================================

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any
import re

@dataclass
class Customer:
    """Entidad Customer con validaciones de negocio"""
    
    # Campos principales
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    sex: Optional[str] = None
    dob: Optional[date] = None
    job_title: Optional[str] = None
    balance: Optional[float] = None
    
    # Campos de auditoría
    created_at: Optional[datetime] = None
    created_ym: Optional[str] = None
    updated_at: Optional[datetime] = field(default_factory=datetime.now)
    
    # Campos adicionales
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_id: Optional[str] = None
    mongo_id: Optional[str] = None
    
    # Regex para validación de email
    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
    
    def __post_init__(self):
        """Validaciones automáticas después de inicialización"""
        self._validate()
        self._derive_fields()
    
    def _validate(self):
        """Validaciones de negocio"""
        # Validar email si existe
        if self.email and not self.EMAIL_PATTERN.match(self.email):
            raise ValueError(f"Email inválido: {self.email}")
        
        # Validar balance si existe
        if self.balance is not None and self.balance < 0:
            raise ValueError("El balance no puede ser negativo")
        
        # Validar sexo si existe
        if self.sex and self.sex.lower() not in ['m', 'f', 'male', 'female', 'masculino', 'femenino']:
            # No lanzar error, solo normalizar
            pass
    
    def _derive_fields(self):
        """Deriva campos automáticamente"""
        # Derivar name si no existe pero hay first_name/last_name
        if not self.name and (self.first_name or self.last_name):
            parts = []
            if self.first_name:
                parts.append(self.first_name.strip())
            if self.last_name:
                parts.append(self.last_name.strip())
            self.name = " ".join(parts) if parts else None
        
        # Derivar created_ym si no existe pero hay created_at
        if not self.created_ym and self.created_at:
            self.created_ym = self.created_at.strftime("%Y-%m")
        
        # Normalizar email
        if self.email:
            self.email = self.email.strip().lower()
        
        # Normalizar phone
        if self.phone:
            self.phone = str(self.phone).strip()
    
    @property
    def full_name(self) -> str:
        """Retorna el nombre completo"""
        if self.name:
            return self.name
        
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        
        return " ".join(parts) if parts else "Sin nombre"
    
    @property
    def age(self) -> Optional[int]:
        """Calcula la edad basada en fecha de nacimiento"""
        if not self.dob:
            return None
        
        today = date.today()
        age = today.year - self.dob.year
        
        # Ajustar si no ha cumplido años este año
        if today.month < self.dob.month or (today.month == self.dob.month and today.day < self.dob.day):
            age -= 1
        
        return age
    
    @property
    def is_valid_email(self) -> bool:
        """Verifica si el email es válido"""
        return bool(self.email and self.EMAIL_PATTERN.match(self.email))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario"""
        data = {}
        
        for field_name, field_value in self.__dict__.items():
            if field_value is not None:
                # Convertir datetime y date a string para serialización
                if isinstance(field_value, datetime):
                    data[field_name] = field_value.isoformat()
                elif isinstance(field_value, date):
                    data[field_name] = field_value.isoformat()
                else:
                    data[field_name] = field_value
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Customer':
        """Crea una instancia Customer desde un diccionario"""
        # Limpiar datos None y vacíos
        clean_data = {}
        
        for key, value in data.items():
            if value is not None and value != "":
                # Convertir strings a datetime/date si es necesario
                if key in ['created_at', 'updated_at'] and isinstance(value, str):
                    try:
                        clean_data[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except:
                        clean_data[key] = value
                elif key == 'dob' and isinstance(value, str):
                    try:
                        clean_data[key] = date.fromisoformat(value)
                    except:
                        clean_data[key] = value
                else:
                    clean_data[key] = value
        
        return cls(**clean_data)
    
    def update_from_dict(self, data: Dict[str, Any]):
        """Actualiza la instancia con datos de un diccionario"""
        for key, value in data.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        
        # Re-validar y re-derivar campos
        self._validate()
        self._derive_fields()
    
    def __str__(self) -> str:
        """Representación string amigable"""
        return f"Customer(id={self.id}, name='{self.full_name}', email='{self.email}')"
    
    def __repr__(self) -> str:
        """Representación técnica"""
        return f"Customer(id={self.id}, name={self.name}, email={self.email})"