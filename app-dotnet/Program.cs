using System;
using System.Data.Common;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Npgsql;
using StackExchange.Redis;

namespace Worker
{
    public class Program
    {
        public static int Main(string[] args)
        {
            try
            {
                var pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
                // var redisConn = OpenRedisConnection("redis");
                // var redis = redisConn.GetDatabase();
                // Establecer la conexión a Redis
                string redisUrl = Environment.GetEnvironmentVariable("REDIS_URL") ?? "redis://localhost:6379";
                var redis_conn = ConnectionMultiplexer.Connect(redisUrl);

                // Obtener una instancia del cliente de Redis
                IDatabase redis = redis_conn.GetDatabase();

                // Keep alive is not implemented in Npgsql yet. This workaround was recommended:
                // https://github.com/npgsql/npgsql/issues/1214#issuecomment-235828359
                var keepAliveCommand = pgsql.CreateCommand();
                keepAliveCommand.CommandText = "SELECT 1";

                // Popular base de datos con 10M

                
                var definition = new { rating = "", user_id = "", movie = "" };
                while (true)
                {
                    // Slow down to prevent CPU spike, only query each 100ms
                    Thread.Sleep(100);

                    // Reconnect redis if down
                    if (redis_conn == null || !redis_conn.IsConnected) {
                        Console.WriteLine("Reconnecting Redis");
                        redis_conn = ConnectionMultiplexer.Connect(redisUrl);
                        redis = redis_conn.GetDatabase();
                    }

                    //RATINGS

                    // string json = redis.StringGet("ratings");
                    /* 
                    if (json != null)
                    {
                        // Deserializar la cadena JSON a un diccionario en C#
                        Dictionary<string, Dictionary<string, double>> datos = JsonConvert.DeserializeObject<Dictionary<string, Dictionary<string, double>>>(json);

                        // Iterar sobre el diccionario y procesar los datos
                        foreach (var usuarioPeliculas in datos)
                        {
                            string user_id = usuarioPeliculas.Key;
                            Dictionary<string, double> peliculasYPuntajes = usuarioPeliculas.Value;

                            foreach (var peliculaPuntaje in peliculasYPuntajes)
                            {
                                string movie = peliculaPuntaje.Key;
                                double rating = peliculaPuntaje.Value;
                                string rating_id = $"{user_id}{movie}";

                                // Aquí puedes realizar la inserción en la base de datos PostgreSQL
                                // Usando el 'usuario', 'pelicula' y 'puntaje'
                                Console.WriteLine($"Rating_id: {rating_id}, Usuario: {user_id}, Película: {movie}, Puntaje: {rating}");

                                // Reconnect DB if down
                                if (!pgsql.State.Equals(System.Data.ConnectionState.Open))
                                {
                                    Console.WriteLine("Reconnecting DB");
                                    pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
                                }
                                else
                                { // Normal +1 vote requested
                                    UpdateRating(pgsql, rating_id, user_id, movie, rating);
                                }
                            }
                        }
                    }
                    else
                    {
                        keepAliveCommand.ExecuteNonQuery();
                    }
                */


                    //KNN
                    RedisValue jsonknn = redis.ListRightPop("knn");
                        
                    if (!jsonknn.IsNullOrEmpty)
                    {
                        JObject jsonObject = JObject.Parse(jsonknn.ToString());
                        foreach (var array in jsonObject.Properties())
                        {
                            string user_id = array.Name;
                            JArray vecinos = (JArray)array.Value;

                            //Console.WriteLine($"user_id: {user_id}");

                            foreach (JArray subArray in vecinos.Cast<JArray>())
                            {
                                string knn_id = Guid.NewGuid().ToString();
                                string vecino = subArray[0].ToString();
                                JToken distancia = subArray[1];

                                //Console.WriteLine($"knn_id: {knn_id}, vecino: {vecino}, Distancia: {distancia}");

                                // Reconnect DB if down
                                if (!pgsql.State.Equals(System.Data.ConnectionState.Open))
                                {
                                    Console.WriteLine("Reconnecting DB");
                                    pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
                                }
                                else
                                { 
                                    UpdateKnn(pgsql, knn_id, user_id, vecino, distancia.Value<double>());
                                }
                            }
                        }
                        
                    }
                    else
                    {
                        keepAliveCommand.ExecuteNonQuery();
                    }


                    //Recomendaciones
                    RedisValue jsonrecs = redis.ListRightPop("rec");
                        
                    if (!jsonrecs.IsNullOrEmpty)
                    {
                        JObject jsonObject = JObject.Parse(jsonrecs.ToString());
                        foreach (var recomendaciones in jsonObject.Properties())
                        {
                            string user_id = recomendaciones.Name;
                            JArray movies = (JArray)recomendaciones.Value;

                            //Console.WriteLine($"user_id: {user_id}");

                            foreach (JArray subArray in movies.Cast<JArray>())
                            {
                                string rec_id = Guid.NewGuid().ToString();
                                string movie = subArray[0].ToString();
                                JToken rating = subArray[1];

                                //Console.WriteLine($"rec_id: {rec_id}, movie: {movie}, Puntaje: {rating}");

                                // Reconnect DB if down
                                if (!pgsql.State.Equals(System.Data.ConnectionState.Open))
                                {
                                    Console.WriteLine("Reconnecting DB");
                                    pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
                                }
                                else
                                { 
                                    UpdateRecs(pgsql, rec_id, user_id, movie, rating.Value<double>());
                                }
                            }
                        }
                        
                    }
                    else
                    {
                        keepAliveCommand.ExecuteNonQuery();
                    }
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine(ex.ToString());
                return 1;
            }
        }

        private static NpgsqlConnection OpenDbConnection(string connectionString)
        {
            NpgsqlConnection connection;

            while (true)
            {
                try
                {
                    connection = new NpgsqlConnection(connectionString);
                    connection.Open();
                    break;
                }
                catch (SocketException)
                {
                    Console.Error.WriteLine("Waiting for db");
                    Thread.Sleep(1000);
                }
                catch (DbException)
                {
                    Console.Error.WriteLine("Waiting for db");
                    Thread.Sleep(1000);
                }
            }

            Console.Error.WriteLine("Connected to db");

            var command = connection.CreateCommand();
            command.CommandText = @"CREATE TABLE IF NOT EXISTS ratings (
                                        rating_id VARCHAR(255) NOT NULL UNIQUE,
                                        user_id VARCHAR(255) NOT NULL,
                                        movie VARCHAR(255) NOT NULL,
                                        rating DOUBLE PRECISION NOT NULL
                                    )";
            command.ExecuteNonQuery();

            return connection;
        }

        private static ConnectionMultiplexer OpenRedisConnection(string hostname)
        {
            // Use IP address to workaround https://github.com/StackExchange/StackExchange.Redis/issues/410
            var ipAddress = GetIp(hostname);
            Console.WriteLine($"Found redis at {ipAddress}");

            while (true)
            {
                try
                {
                    Console.Error.WriteLine("Connecting to redis");
                    return ConnectionMultiplexer.Connect(ipAddress);
                }
                catch (RedisConnectionException)
                {
                    Console.Error.WriteLine("Waiting for redis");
                    Thread.Sleep(1000);
                }
            }
        }

        private static string GetIp(string hostname)
            => Dns.GetHostEntryAsync(hostname)
                .Result
                .AddressList
                .First(a => a.AddressFamily == AddressFamily.InterNetwork)
                .ToString();

        private static void UpdateRating(NpgsqlConnection connection, string rating_id, string user_id, string movie, double rating)
        {
            var command = connection.CreateCommand();
            try
            {
                command.CommandText = "INSERT INTO ratings (rating_id, user_id, movie, rating) VALUES (@rating_id, @user_id, @movie, @rating)";
                command.Parameters.AddWithValue("@rating_id", rating_id);
                command.Parameters.AddWithValue("@user_id", user_id);
                command.Parameters.AddWithValue("@movie", movie);
                command.Parameters.AddWithValue("@rating", rating);
                command.ExecuteNonQuery();
            }
            catch (DbException)
            {
                command.CommandText = "UPDATE ratings SET rating = @rating WHERE rating_id = @rating_id";
                command.ExecuteNonQuery();
            }
            finally
            {
                command.Dispose();
            }
        }

        private static void UpdateRecs(NpgsqlConnection connection, string rec_id, string user_id, string movie, double rating)
        {
            var command = connection.CreateCommand();
            try
            {
                command.CommandText = $@"CREATE TABLE IF NOT EXISTS rec{user_id} (
                                        rec_id VARCHAR(255) NOT NULL UNIQUE,
                                        user_id VARCHAR(255) NOT NULL,
                                        movie VARCHAR(255) NOT NULL,
                                        rating DOUBLE PRECISION NOT NULL
                                    )";
                command.ExecuteNonQuery();

                command.CommandText = $"INSERT INTO rec{user_id} (rec_id, user_id, movie, rating) VALUES (@rec_id, @user_id, @movie, @rating)";
                command.Parameters.AddWithValue("@rec_id", rec_id);
                command.Parameters.AddWithValue("@user_id", user_id);
                command.Parameters.AddWithValue("@movie", movie);
                command.Parameters.AddWithValue("@rating", rating);
                command.ExecuteNonQuery();
            }
            catch (DbException)
            {
                command.CommandText = $"UPDATE rec{user_id} SET rating = @rating WHERE rec_id = @rec_id";
                command.ExecuteNonQuery();
            }
            finally
            {
                command.Dispose();
            }
        }

        private static void UpdateKnn(NpgsqlConnection connection, string knn_id, string user_id, string vecino, double distancia)
        {
            var command = connection.CreateCommand();
            try
            {
                command.CommandText = $@"CREATE TABLE IF NOT EXISTS knn{user_id} (
                                        knn_id VARCHAR(255) NOT NULL UNIQUE,
                                        user_id VARCHAR(255) NOT NULL,
                                        vecino VARCHAR(255) NOT NULL,
                                        distancia DOUBLE PRECISION NOT NULL
                                    )";
                command.ExecuteNonQuery();

                command.CommandText = $"INSERT INTO knn{user_id} (knn_id, user_id, vecino, distancia) VALUES (@knn_id, @user_id, @vecino, @distancia)";
                command.Parameters.AddWithValue("@knn_id", knn_id);
                command.Parameters.AddWithValue("@user_id", user_id);
                command.Parameters.AddWithValue("@vecino", vecino);
                command.Parameters.AddWithValue("@distancia", distancia);
                command.ExecuteNonQuery();
            }
            catch (DbException)
            {
                command.CommandText = $"UPDATE knn{user_id} SET distancia = @distancia WHERE knn_id = @knn_id";
                command.ExecuteNonQuery();
            }
            finally
            {
                command.Dispose();
            }
        }
    }
}