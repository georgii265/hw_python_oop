class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float, 
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        
    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')
        

class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    
    def __init__(self, action: int, duration: float, weight: float,) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM  
        
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration
        
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        messages = InfoMessage(self.__class__.__name__, self.duration,
                               self.get_distance(), self.get_mean_speed(),
                               self.get_spent_calories())
        return messages
        

class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20
    
    def get_spent_calories(self) -> float:
        """Метод расчёта калорий, его нужно переопределить."""
        return(self.COEFF_CALORIE_1
               * self.get_mean_speed()
               - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM * self.duration
        

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    NUM_COEFF_SW_1 = 0.035
    NUM_COEFF_SW_2 = 0.029

    def __init__(self, action: int, duration: float, 
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
    
    def get_spent_calories(self) -> float:
        """Расчёт калорий для этого класса должен проводиться по такой формуле"""
        return(self.NUM_COEFF_SW_1 * self.weight
               + (self.get_mean_speed()**2 // self.height) 
               * self.NUM_COEFF_SW_2 * self.weight) * self.duration
        

class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    NUM_COEFF_S_1 = 1.1
    NUM_COEFF_S_2 = 2

    def __init__(self, action: int, duration: float, weight: float, 
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    
    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * Swimming.LEN_STEP) / Training.M_IN_KM
    
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return(self.length_pool * self.count_pool / Training.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return((self.get_mean_speed() + self.NUM_COEFF_S_1) * self.NUM_COEFF_S_2 * self.weight) 


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_train = {'SWM': Swimming, 
                  'RUN': Running,
                  'WLK': SportsWalking
                }
    return type_train[workout_type](*data)
    

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)