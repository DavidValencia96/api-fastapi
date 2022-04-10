-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-04-2022 a las 13:07:48
-- Versión del servidor: 10.4.17-MariaDB
-- Versión de PHP: 7.4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `api-jd`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comments`
--

CREATE TABLE `comments` (
  `comment_id` int(11) NOT NULL,
  `tweet_id` int(11) DEFAULT NULL,
  `comment_content` varchar(255) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL,
  `cm_create_date` varchar(30) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL,
  `cm_update_date` varchar(30) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL,
  `user_id_comment` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_nopad_ci;

--
-- Volcado de datos para la tabla `comments`
--

INSERT INTO `comments` (`comment_id`, `tweet_id`, `comment_content`, `cm_create_date`, `cm_update_date`, `user_id_comment`) VALUES
(1, 1, 'Comentario editado desde postman sin el edit al tweet', '2022-04-07', '2022-04-09', 0),
(2, 1, 'Comentario', '2022-04-07', '2022-04-07', 0),
(3, 1, 'Comentario', '2022-04-07', '2022-04-07', 0),
(6, 3, 'Comentario', '2022-04-07', '2022-04-07', 0),
(9, 12, 'Comentario de tweet 12', '2022-04-09', '2022-04-09', 12),
(10, 2, 'Comentario editado desde postman sin el edit al tweet', '2022-04-09', '2022-04-09', 12),
(11, 12, 'Comentario de tweet 12', '2022-04-09', '2022-04-09', 12);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tweet`
--

CREATE TABLE `tweet` (
  `tweet_id` int(11) NOT NULL,
  `content` varchar(255) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL,
  `create_tw_date` varchar(30) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL,
  `update_tw_date` varchar(30) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL,
  `user_id_create` varchar(30) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_nopad_ci;

--
-- Volcado de datos para la tabla `tweet`
--

INSERT INTO `tweet` (`tweet_id`, `content`, `create_tw_date`, `update_tw_date`, `user_id_create`) VALUES
(4, 'contenido del tweet', '2022-04-07', '2022-04-09', '0'),
(5, 'contenido del tweet pero modificado', '2022-04-07', '2022-04-08', '0'),
(6, 'contenido del tweet', '2022-04-07', '2022-04-07', '0'),
(7, 'modificado desde postman v2', '2022-04-07', '2022-04-09', '0'),
(8, 'contenido del tweet', '2022-04-07', '2022-04-07', '0'),
(9, 'contenido del tweet desde postman', '2022-04-09', '2022-04-09', '17');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL,
  `country` varchar(30) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL,
  `phone` varchar(10) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL,
  `email` varchar(50) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL,
  `password` varchar(50) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL,
  `user_create` varchar(20) COLLATE utf8mb4_general_nopad_ci DEFAULT NULL,
  `tipo_user` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_nopad_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name`, `country`, `phone`, `email`, `password`, `user_create`, `tipo_user`) VALUES
(1, 'juan -- postman', 'Colombia', '3123456xx', 'david@david.com', 'gAAAAABiUVV_EUvdxhjUf0CvL2OesrLlV7_zc_ZlbgQacqFdce', '2022-04-07', 2022),
(8, 'juan David Valencia', 'Colombia', '3123456789', 'user@exasmple.com', 'gAAAAABiTk9AuKySDqDtcStTZr-c0dYV34tYt6kRbWgmotEQ1I', '2022-04-07', 2022),
(9, 'juan David Valencia', 'Colombia', '1246566', 'juan@example.com', 'juandavid', '2022-04-07', 2022),
(10, 'maria alejandra c c', 'Colombia', '3123456789', 'user@exsssample.com', 'gAAAAABiTqcrYHs07j8E5pG52IoKszb3HOI1fSJIy4jtPQQ2yE', '2022-04-07', 2022),
(11, 'prueba de token', 'Colombia', '2332222', 'juan@d1.com', 'gAAAAABiT7hraNeAGDVvEJSa7Y_K6CRhPJ9_W37P1gna8Uukcc', '2022-04-07', 2022),
(12, 'prueba de token', 'Colombia', '2332222', 'juan@d1.com', 'gAAAAABiT8JYHxKKvqd-bqNMXEyMSq_Ss5PF9mWmA-G7Y8BV7x', '2022-04-07', 2022),
(13, 'prueba de token', 'Colombia', '2332222', 'juan@d1.com.com', 'gAAAAABiT8JaRd3gsNfOUoxibWLWlLnaVQlONdR46t6YRTLGeo', '2022-04-07', 2022),
(14, 'prueba de token', 'Colombia', '2332222', 'juan@d2.com', 'gAAAAABiUUfeVnx1RIPfJKsHZcM7nT2fEpF0Y8FRFNKnKHbOAK', '2022-04-07', 2022),
(15, 'prueba de token', 'Colombia', '2332222', 'juan@d2.com', 'gAAAAABiUUgPNcqKwCH-pg37iW2AhUogX-eD_2QrnWhaxE7res', '2022-04-07', 2022),
(16, 'xxxxxxx', 'españa', '31234567xx', 'juan@d3.com', 'gAAAAABiUVExn6HA31KlBC1Ln_wCL9MHL7nAajgu3u-KXwnzWf', '2022-04-07', 2022),
(18, 'juan David Valencia postamn', 'Colombia', '3123456789', 'user@example.es', 'gAAAAABiUVYXurTGprimiS1bUVO3I48FWmeU82R1viDyGMgfXo', '2022-04-09', 2022),
(19, 'juan David Valencia postamn v2', 'Colombia', '3123456789', 'user@example.es', 'gAAAAABiUVYnzHz_MNBRrder_kUyTUgaI_GgTdi4SwHDf2d8SD', '2022-04-09', 2022);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`comment_id`);

--
-- Indices de la tabla `tweet`
--
ALTER TABLE `tweet`
  ADD PRIMARY KEY (`tweet_id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `comments`
--
ALTER TABLE `comments`
  MODIFY `comment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `tweet`
--
ALTER TABLE `tweet`
  MODIFY `tweet_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
