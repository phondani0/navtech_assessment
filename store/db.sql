create table `products` ( id int not null auto_increment, name varchar(255) not null, price int not null, primary key(id));



create table users (id int not null auto_increment, name varchar(100), email varchar(100) not null, password varchar(255) not null, primary key(id));



create table orders(id int not null auto_increment, user_id int not null, primary key(id), foreign key(user_id) references users(id));



create table order_product(id int not null auto_increment, order_id int n
ot null,product_id int not null, quantity int not null, primary key(id), foreign
 key(order_id) references orders(id), foreign key(product_id) references products(id));