# Método de login corregido para usar el procedimiento adecuado según el input
@strawberry.mutation
def login(self, email: str, password: str) -> UserResponse:
    try:
        # Determinar si el input es un email o un username
        is_email = '@' in email
        
        # Usar el procedimiento almacenado adecuado (login_email o user_login)
        if is_email:
            # Si parece un email, usamos login_email
            rows = Database.execute_proc("login_email", email, password)
        else:
            # Si no parece un email, asumimos que es un username
            rows = Database.execute_proc("user_login", email, password)
        
        if not rows or not rows[0]['is_valid']:
            logger.error(f"Login fallido: Usuario no encontrado o credenciales incorrectas - {email}")
            return UserResponse(
                error=ErrorResponse(
                    message="Credenciales incorrectas",
                    code=401
                )
            )

        # Extraer los datos del usuario de la respuesta
        user_data = row_to_dict(rows[0])
        
        # Login exitoso - registrar
        logger.info(f"Login exitoso: {email}")
        
        # Registrar el intento de login exitoso en la tabla de auditoría
        Database.execute_proc(
            "audit_login_attempt",
            user_data['username'],
            "localhost",  # IP placeholder
            "API Client",  # User-Agent placeholder
            True          # Login exitoso
        )
        
        # Retornar los datos del usuario exitosamente
        return UserResponse(
            user=User(
                id=user_data['user_id'],
                username=user_data['username'],
                email=user_data['email'],
                firstname=user_data['firstname'],
                lastname=user_data['lastname'],
                confirmed=True,  # Valor por defecto para usuarios que pueden hacer login
                deleted=False,   # Un usuario no borrado
                suspended=False, # Un usuario no suspendido
                institution=None,
                department=None,
                timecreated=datetime.now(),  # Placeholder
                timemodified=datetime.now()  # Placeholder
            )
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return UserResponse(
            error=ErrorResponse(
                message=f"Error interno: {str(e)}",
                code=500
            )
        )
