<!DOCTYPE html>
<html>
<head>
    <title>Sistema de recomendación películas</title>
</head>
<body>
    <h1>Sistema de recomendación películas</h1>

    <form method="POST">
        <input type="submit" name="cargar_datos" value="Cargar conjunto de datos"><br><br>

        <label for="usuario">ID de Usuario:</label>
        <input type="text" id="usuario" name="usuario" placeholder="Ingrese el ID de Usuario"><br><br>

        <label for="distancia">Distancia utilizada:</label>
        <input type="text" id="distancia" name="distancia" placeholder="Ingrese la Distancia utilizada"><br><br>

        <input type="submit" name="vecino_cercano" value="Cargar vecino más cercano"><br><br>

        <label for="n_knn">Número de knn:</label>
        <input type="text" id="n_knn" name="n_knn" placeholder="Ingrese el Número de knn"><br><br>

        <label for="n_items">Número de items a recomendar:</label>
        <input type="text" id="n_items" name="n_items" placeholder="Ingrese el Número de items a recomendar"><br><br>

        <input type="submit" name="recomendar_peliculas" value="Recomendar películas"><br><br>
    </form>

    <?php
    $api_endpoint = $_ENV["API_ENDPOINT"] ?: "http://localhost:5000/api/";
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (isset($_POST['cargar_datos'])) {
            $output = exec("curl -i ${api_endpoint}cargar");
            echo "<pre>$output</pre>";
        } elseif (isset($_POST['vecino_cercano']) && isset($_POST['usuario']) && isset($_POST['distancia'])) {

            $counter = 0;

            $usuario = $_POST['usuario'];
            $distancia = $_POST['distancia'];
            $output = exec("curl -i ${api_endpoint}knn/$usuario/$distancia");
            
            $data = json_decode($output, true);
            if(!empty($data)){
                echo '<table border="1">
                        <tr>
                            <th>Usuario</th>
                            <th>Distancia</th>
                        </tr>';
                foreach ($data as $item) {

                    if ($counter >= 10) {
                        break;
                    }

                    echo '<tr>';
                    echo '<td>' . $item[0] . '</td>';
                    echo '<td>' . $item[1] . '</td>';
                    echo '</tr>';

                    $counter++;
                }
                echo '</table>';
            } else {
                echo 'No se recibieron datos válidos.';
            }
        } elseif (isset($_POST['recomendar_peliculas']) && isset($_POST['usuario']) && isset($_POST['distancia']) && isset($_POST['n_knn']) && isset($_POST['n_items'])) {
            $usuario = $_POST['usuario'];
            $distancia = $_POST['distancia'];
            $n_knn = $_POST['n_knn'];
            $n_items = $_POST['n_items'];
            $output = exec("curl -i ${api_endpoint}recommend/$usuario/$distancia/$n_knn/$n_items");
            
            $data = json_decode($output, true);
            if(!empty($data)){
                echo '<table border="1">
                        <tr>
                            <th>Película</th>
                            <th>Puntaje</th>
                        </tr>';
                foreach ($data as $item) {
                    echo '<tr>';
                    echo '<td>' . $item[0] . '</td>';
                    echo '<td>' . $item[1] . '</td>';
                    echo '</tr>';
                }
                echo '</table>';
            } else {
                echo 'No se recibieron datos válidos.';
            }
        }
    }
    ?>
</body>
</html>
