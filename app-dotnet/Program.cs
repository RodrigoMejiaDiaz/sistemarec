using System;
using System.Data.Common;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Newtonsoft.Json;
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
                string redisUrl = Environment.GetEnvironmentVariable("REDIS_URL") ?? "localhost:6379";
                var redis_conn = ConnectionMultiplexer.Connect(redisUrl);

                // Obtener una instancia del cliente de Redis
                IDatabase redis = redis_conn.GetDatabase();

                // Keep alive is not implemented in Npgsql yet. This workaround was recommended:
                // https://github.com/npgsql/npgsql/issues/1214#issuecomment-235828359
                var keepAliveCommand = pgsql.CreateCommand();
                keepAliveCommand.CommandText = "SELECT 1";

                // Popular base de datos con 10M

                /* 
                var definition = new { rating = "", user_id = "", movie = "" };
                while (true)
                {
                    // Slow down to prevent CPU spike, only query each 100ms
                    Thread.Sleep(5000);

                    // Reconnect redis if down
                    if (redis_conn == null || !redis_conn.IsConnected) {
                        Console.WriteLine("Reconnecting Redis");
                        redis_conn = ConnectionMultiplexer.Connect(redisUrl);
                        redis = redis_conn.GetDatabase();
                    }
                    // string json = redis.StringGet("ratings");
                    string json = redis.StringGet("");
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
                }
                */
                
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
    }
}