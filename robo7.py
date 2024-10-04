import os
import datetime
import re
from roboflow import Roboflow
from openpyxl import Workbook


class ImageProcessor:
    def __init__(self, api_key, project_name, version_number, proximity_threshold):
        self.rf = Roboflow(api_key=api_key)
        self.project = self.rf.workspace().project(project_name)
        self.model = self.project.version(version_number).model
        self.proximity_threshold = proximity_threshold

    def is_near(self, pred1, pred2):
        return abs(pred1['x'] - pred2['x']) < self.proximity_threshold and abs(pred1['y'] - pred2['y']) < self.proximity_threshold

    def get_image_creation_datetime(self, image_path):
        creation_time = os.path.getctime(image_path)
        return datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')

    def filter_predictions(self, predictions):
        filtered_predictions = []
        for pred in predictions['predictions']:
            found = False
            for group in filtered_predictions:
                if self.is_near(pred, group[0]):
                    existing_classes = [p['class'] for p in group]
                    if pred['class'] == '2' and '7' in existing_classes:
                        group[0] = pred
                    elif pred['class'] == '7' and '2' in existing_classes:
                        group[0] = next(p for p in group if p['class'] == '2')
                    elif pred['confidence'] > group[0]['confidence']:
                        group[0] = pred
                    found = True
                    break
            if not found:
                filtered_predictions.append([pred])
        return [group[0] for group in filtered_predictions]

    def predict_image(self, image_path):
        predictions = self.model.predict(
            image_path, confidence=8, overlap=50).json()
        filtered_predictions = self.filter_predictions(predictions)
        sorted_predictions = sorted(filtered_predictions, key=lambda p: p['x'])
        classes = [pred['class'] for pred in sorted_predictions]
        if len(classes) > 2:
            result_string = ''.join(classes[:-2]) + '.' + ''.join(classes[-2:])
        else:
            result_string = '.'.join(classes)
        return result_string

    def process_images(self, image_folder):
        image_files = [f for f in os.listdir(
            image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        results = []

        for image_file in image_files:
            image_path = os.path.join(image_folder, image_file)
            creation_datetime = self.get_image_creation_datetime(image_path)
            result_string = self.predict_image(image_path)
            results.append((image_file, creation_datetime, result_string))

        # Ordenar los resultados por el nombre del archivo de imagen numéricamente
        results.sort(key=lambda x: int(re.findall(r'\d+', x[0])[0]))

        # Crear el archivo Excel y agregar los datos ordenados
        excel_filename = os.path.join(image_folder, "predictions.xlsx")
        wb = Workbook()
        ws = wb.active
        ws.title = "Predictions"

        for result in results:
            ws.append(result)

        wb.save(excel_filename)
        print(f"Los resultados han sido guardados en {excel_filename}")


if __name__ == "__main__":
    image_folder = "C:\\Users\\Dione\\Downloads\\1. CIDIMEC\\PresentaciónFinal\\prueba3"
    api_key = "6iUlqDVylBlNgJyO6AaW"
    project_name = "dial-comparator-detection"
    version_number = 1
    proximity_threshold = 38

    processor = ImageProcessor(
        api_key, project_name, version_number, proximity_threshold)
    processor.process_images(image_folder)
