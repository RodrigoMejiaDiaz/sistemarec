<!DOCTYPE html>
<html>
<head>
    <title>Interfaz de Acceso a API</title>
</head>
<body>
    <h1>Interfaz de Acceso a API</h1>

    <form method="POST">
        <input type="submit" name="cargar_datos" value="Cargar conjunto de datos"><br><br>

        <label for="usuario">ID de Usuario:</label>
        <input type="text" id="usuario" name="usuario" placeholder="Ingrese el ID de Usuario"><br><br>

        <input type="submit" name="vecino_cercano" value="Cargar vecino más cercano">
        <input type="submit" name="recomendar_peliculas" value="Recomendar películas"><br><br>
    </form>

    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (isset($_POST['cargar_datos'])) {
            $output = exec('curl -i http://app-python:5000/api/cargar');
            echo "<pre>$output</pre>";
        } elseif (isset($_POST['vecino_cercano']) && isset($_POST['usuario'])) {
            $usuario = $_POST['usuario'];
            $output = exec("curl -i http://app-python:5000/api/knn/$usuario/pearson");
            echo "<pre>$output</pre>";
        } elseif (isset($_POST['recomendar_peliculas']) && isset($_POST['usuario'])) {
            $usuario = $_POST['usuario'];
            $output = exec("curl -i http://app-python:5000/api/recommend/$usuario/pearson/1/5");
            echo "<pre>$output</pre>";
        }
    }
    ?>
</body>
</html>
