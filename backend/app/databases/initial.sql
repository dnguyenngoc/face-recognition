
--  1. Create role
INSERT 
	INTO shop.role(id, code, name, create_date, update_date) 
	VALUES ('1', 'boss', 'super boss', '2021-06-28', null)
	ON CONFLICT (code)
	DO UPDATE SET name = EXCLUDED.name, create_date = EXCLUDED.create_date, update_date = EXCLUDED.update_date
;

--  1. Create user
INSERT 
	INTO shop."user" (id, user_name, first_name, last_name, full_name, email, phone, password, role_id, create_date, update_date)
	VALUES ('1', 'duynguyenngoc', 'Duy', 'Nguyen', 'Duy Nguyen Ngoc', 'duynguyenngoc@hotmail.com', '+84399360638', '1q2w3e4r', 1, '2021-06-28', null)
	ON CONFLICT (user_name)
	DO UPDATE SET first_name = EXCLUDED.first_name, 
				  last_name = EXCLUDED.last_name,
				  email = EXCLUDED.email,
				  phone = EXCLUDED.phone,
				  password = EXCLUDED.password,
				  role_id = EXCLUDED.role_id,
				  create_date = EXCLUDED.create_date
;