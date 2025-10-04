###LOAD FIRST tarea2.sql and region-comuna.sql in mysql  
#mysql -uroot -p < tarea2.sql
#mysql -uroot -p tarea2 < region-comuna.sql
CREATE USER 'cc5002'@'localhost' identified by 'programacionweb';
GRANT ALL PRIVILEGES ON tarea2.* To 'cc5002'@'localhost';
FLUSH PRIVILEGES;

###Create avisos to test webpage, run all
INSERT INTO tarea2.aviso_adopcion (fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion) VALUES ("2025-08-15 12:34", 130207, "Costanera center", "Horst Paulmann", "Jumbo@cencosud.com", "+569.87654321","gato",3,2,"m","2025-08-15 15:45","Hace algo?");
INSERT INTO tarea2.aviso_adopcion (fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion) VALUES ("2025-08-17 09:23", 130208, "La Moneda", "Gabriel Boric", "info@gobierno.com", "+569.00000133","gato",2,1,"a","2025-08-17 14:30","va por la re-candidatura");
INSERT INTO tarea2.aviso_adopcion (fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion) VALUES ("2025-08-20 13:50", 130211, "El lider", "Nicolás Ibáñez", "lider@walmart.com", "+569.56781234","perro",1,9,"a","2025-08-21 10:00","Cuanta facha");
INSERT INTO tarea2.aviso_adopcion (fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion) VALUES ("2025-08-24 21:07", 130229, "Meiggs", "José Reyes", "rey@meiggs.com", "+569.11112222","gato",2,2,"a","2025-08-25 12:15","lo buscan!!");
INSERT INTO tarea2.aviso_adopcion (fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion) VALUES ("1428-10-31 23:59", 50202, "Castilo de dracula", "Bram Stoker", "dra@cula.com", "+569.66666666","gato",1,579,"a","1897-05-26 00:00","No hace nada!!!");
INSERT INTO tarea2.foto (ruta_archivo, nombre_archivo, aviso_id) VALUES ("static/uploads", "Dracula.jpeg", 5);
INSERT INTO tarea2.foto (ruta_archivo, nombre_archivo, aviso_id) VALUES ("static/uploads", "Dracula-2.jpeg", 5);
INSERT INTO tarea2.foto (ruta_archivo, nombre_archivo, aviso_id) VALUES ("static/uploads", "Dracula-3.jpeg", 5);
INSERT INTO tarea2.foto (ruta_archivo, nombre_archivo, aviso_id) VALUES ("static/uploads", "3Gatos.jpeg", 1);
INSERT INTO tarea2.foto (ruta_archivo, nombre_archivo, aviso_id) VALUES ("static/uploads", "1Perro.jpeg", 3);
INSERT INTO tarea2.foto (ruta_archivo, nombre_archivo, aviso_id) VALUES ("static/uploads", "2Gatos.jpeg", 2);
INSERT INTO tarea2.foto (ruta_archivo, nombre_archivo, aviso_id) VALUES ("static/uploads", "2Gatos-2.jpeg", 4);
INSERT INTO tarea2.foto (ruta_archivo, nombre_archivo, aviso_id) VALUES ("static/uploads", "2Gatos-2.jpeg", 2);
INSERT INTO tarea2.foto (ruta_archivo, nombre_archivo, aviso_id) VALUES ("static/uploads", "2Gatos-3.jpeg", 2);