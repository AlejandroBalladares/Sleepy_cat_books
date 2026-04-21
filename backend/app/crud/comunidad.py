from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy import Sequence
from app.models.comunidad import Comunidad, ComunidadCrear, ComunidadActualizar, UsuarioComunidad
from app.models.comunidad import ComunidadFiltro, PublicacionCrear, Publicacion, ImagenPublicacion
from app.models.users import Usuario

class ServicioComunidad(object):
    def create_community(session: Session, community_create: ComunidadCrear) -> Comunidad:
        
        if session.exec(select(Comunidad).where(Comunidad.nombre == community_create.nombre)).first():
            raise HTTPException(status_code=400, detail="Ya existe una comunidad con este nombre")

        community_obj = Comunidad.model_validate(community_create) 
        print(community_obj)
        session.add(community_obj)
        session.commit()
        session.refresh(community_obj)

        member_obj = UsuarioComunidad(id_usuario=community_obj.id_creador, id_comunidad=community_obj.id)
        session.add(member_obj)
        session.commit()

        return community_obj

    # Devuelve las comunidades que coincidan con el filtro
    def get_communities_by_filter(session: Session, community_filter: ComunidadFiltro) -> Sequence[Comunidad]:
        comunidades = select(Comunidad)

        if community_filter.nombre is not None:
            comunidades = comunidades.where(Comunidad.nombre.ilike(f"%{community_filter.nombre}%"))

        return session.exec(comunidades).all()

    def get_community_by_id(session: Session, id_comunidad: int) -> Comunidad:
        community = session.exec(select(Comunidad).where(Comunidad.id == id_comunidad)).first()
        if not community:
            raise HTTPException(status_code=404, detail="No existe comunidad")
        return community
    

    def edit_community(session: Session, current_user: Usuario, community_id: int, community_edit: ComunidadActualizar) -> Comunidad:
        community = session.exec(select(Comunidad).where(Comunidad.id == community_id, Comunidad.id_creador == current_user.id)).first()

        if not community:
            raise HTTPException(status_code=403, detail="Usuario no tiene permiso para editar esta comunidad")

        community_data = community_edit.model_dump(exclude_unset=True)
        community.sqlmodel_update(community_data) 
        
        if community_edit.nombre is not None:
            community.nombre = community_edit.nombre

        if community_edit.tipo is not None:
            community.tipo = community_edit.tipo

        if community_edit.descripcion is not None:
            community.descripcion = community_edit.descripcion
        
        if community_edit.imagen is not None:
            community.imagen = community_edit.imagen
        
        session.add(community)
        session.commit()
        session.refresh(community)
        
        return community
    
    def add_member_to_community(session: Session, current_user: Usuario, community_id: int) -> Comunidad:
        community = session.exec(select(Comunidad).where(Comunidad.id == community_id)).first()

        if not community:
            raise HTTPException(status_code=404, detail="No existe la comunidad")

        if community.id_creador == current_user.id:
            raise HTTPException(status_code=400, detail="Usuario ya pertenece a la comunidad")
      
        member = session.exec(select(UsuarioComunidad).where(UsuarioComunidad.id_usuario == current_user.id, UsuarioComunidad.id_comunidad == community_id)).first()

        if member:
            raise HTTPException(status_code=400, detail="Usuario ya pertenece a la comunidad")

        new_member = UsuarioComunidad(id_usuario=current_user.id, id_comunidad=community.id)

        session.add(new_member)
        session.commit()
        session.refresh(new_member)

        return community
        
    def get_members(session: Session, community_id: int) -> Sequence[Usuario]:
        return session.exec(select(Usuario).join(UsuarioComunidad, UsuarioComunidad.id_usuario == Usuario.id).where(UsuarioComunidad.id_comunidad == community_id)).all()        

    def add_post(session: Session, current_user: Usuario, community_id: int, post_create: PublicacionCrear) -> Publicacion:
        community = session.exec(select(Comunidad).where(Comunidad.id == community_id)).first()

        if not community:
            raise HTTPException(status_code=404, detail="No existe la comunidad")

        member = session.exec(select(UsuarioComunidad).where(UsuarioComunidad.id_usuario == current_user.id, UsuarioComunidad.id_comunidad == community_id)).first()

        if member is None:
            raise HTTPException(status_code=403, detail="Usuario no pertenece a la comunidad")

        imagenes = [ImagenPublicacion(url=url) for url in post_create.imagenes if url is not None]
        new_post = Publicacion.model_validate(
            post_create,
            update={"id_usuario": current_user.id, "id_comunidad": community.id, "usuario": current_user, "imagenes": imagenes}
        )

        session.add(new_post)
        session.commit()
        session.refresh(new_post)

        return new_post
    
    def get_posts(session: Session, community_id: int) -> Sequence[Publicacion]:
        return session.exec(select(Publicacion).join(Comunidad, Comunidad.id == Publicacion.id_comunidad).where(Publicacion.id_comunidad == community_id)).all()  