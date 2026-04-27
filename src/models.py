from dataclasses import dataclass
from datetime import datetime
from typing import List
import math

@dataclass
class GPSPoint:
    lat: float
    lon: float
    alt: float
    time: float  # Using float for elapsed seconds as per assignment

class Car:
    """
    Domain logic representing a vehicle traversing a set of GPS points.
    Responsible for calculating accumulated metrics like distance and duration.
    """
    def __init__(self, gps_points: List[GPSPoint]):
        if not gps_points:
            raise ValueError("Cannot initialize Car with an empty list of GPS points.")
        self.route = gps_points

    def get_total_distance(self) -> float:
        """Calculates total distance traveled across the entire route in kilometers."""
        return sum(
            self.calculate_distance(p1, p2)
            for p1, p2 in zip(self.route[:-1], self.route[1:])
        )
        
    def calculate_distance(self, p1: GPSPoint, p2: GPSPoint) -> float:
        """Haversine formula to calculate distance between two lat/lon points in kilometers."""
        R = 6371.0 
        lat1, lon1 = math.radians(p1.lat), math.radians(p1.lon)
        lat2, lon2 = math.radians(p2.lat), math.radians(p2.lon)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    
    def get_duration(self) -> float:
        """Calculates total duration of the track in seconds."""
        if not self.route:
            return 0.0
        return self.route[-1].time - self.route[0].time
    
    def get_distance_up_to(self, end_index: int) -> float:
        """Calculates distance traveled up to a specific point index."""
        if end_index <= 0 or end_index >= len(self.route):
            return 0.0
        
        distance = 0.0
        for i in range(end_index):
            p1 = self.route[i]
            p2 = self.route[i+1]
            distance += self.calculate_distance(p1, p2)
        return distance
