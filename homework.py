"""dataclasses - Классы данных"""
from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    VMIN: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Метод расчёта калорий, его нужно переопределить."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # функция ничего ни делает
        raise NotImplementedError(self.__class__.__name__ + '.get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__, self.duration,
                              self.get_distance(), self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    FIRST_COEFF_CALORIE: float = 18
    SECOND_COEFF_CALORIE: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.FIRST_COEFF_CALORIE * self.get_mean_speed()
                - self.SECOND_COEFF_CALORIE) * self.weight / self.M_IN_KM
                * (self.duration * self.VMIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    FIRST_COEFF_CALORIE: float = 0.035
    SECOND_COEFF_CALORIE: float = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.FIRST_COEFF_CALORIE * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.SECOND_COEFF_CALORIE
                * self.weight) * (self.duration * self.VMIN)


class Swimming(Training):
    """Тренировка: плавание."""
    FIRST_COEFF_CALORIE: float = 1.1
    SECOND_COEFF_CALORIE: int = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.FIRST_COEFF_CALORIE)
                * self.SECOND_COEFF_CALORIE * self.weight)


def read_package(workout: str, parameters: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_parameters: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    return training_parameters[workout](*parameters)


def main(trainings) -> None:
    """Главная функция."""
    info = trainings.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, parametrs in packages:
        training = read_package(workout_type, parametrs)
        main(training)
