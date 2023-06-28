from os import mkdir
import errno

ruta_proyecto = input('Ingrese la ruta donde esta la carpeta Funcionalidades:\n')
entidad_plural = input('Ingrese la entidad en plural:\n')
entidad_singular = input('Ingrese la entidad en singular:\n')
entidad_singular_m =  entidad_singular.lower()
carpetas = [
    'ActivarInactivar',
    'Consultar',
    'ConsultarPorId',
    'Crear',
    'Editar',
    'Especificacion',
    'LogicaNegocio',
    'Repositorio']
carpeta_funcion = f'{ruta_proyecto}\{entidad_plural}'
complementos_command = [ 'Command', 'CommandHandler' ]
complementos_query = ['Query', 'QueryHandler']
complementos = [ 'Controller', 'Response']
complementos_command.extend(complementos)
complementos_query.extend(complementos)
    
name_space = f'namespace SEG.MENU.Aplicacion.Funcionalidades.{entidad_plural}'
u_mediat_r = 'using MediatR;\n'
u_entidad = name_space.replace('namespace', 'using')
u_logica_negocio = name_space.replace('namespace', 'using') + '.LogicaNegocio;\n'
u_microsoft = 'using Microsoft.AspNetCore.Mvc;\n'
u_seg_comun = 'using SEG.Comun.General;\n'
u_seg_menu_entidades = 'using SEG.MENU.Dominio.Entidades;\n'
u_unit_of_work = 'using SEG.MENU.Infraestructura.UnidadTrabajo;\n'
p_record = 'public record struct '
p_class = 'public class '
p_interface = 'public interface '
p_readonly = 'private readonly '
p_async_task = 'public async Task'
a_route = '[Route("api/[controller]")]\n'
a_controller = '[ApiController]\n'
i_gestion = f'IGestion{entidad_plural}'
c_gestion = f'_gestion{entidad_plural}'
v_gestion = f'gestion{entidad_plural}'
cancel_token = 'CancellationToken cancellationToken'
i_mediator_ctor = '(IMediator mediator) => _mediator = mediator;\n'
i_unit_work_write = 'IUnitOfWorkSegEscritura '
i_repo_lectura = f'I{entidad_singular}RepositorioLectura ' 
i_repo_escritura = f'I{entidad_singular}RepositorioEscritura '
v_repo_lectura =  f'{entidad_singular_m}Lectura'
v_repo_escritura = f'{entidad_singular_m}Escritura'
n = '\n'
n_n = '\n\n'
_ = '    '
lla = '\n{\n' + _
lla2 = n + _ + '{' + n + _*2
llc = '\n}'
llc2 = n + _ + '}'
a_resp = f'{n + _}[ProducesResponseType(StatusCodes.Status200OK)]{n + _}[ProducesResponseType(StatusCodes.Status400BadRequest)]{n + _}'

clases_repo = [ f'{entidad_singular}RepositorioLectura', f'{entidad_singular}RepositorioEscritura']

def crear_carpetas(rutaCarpeta, carpetas):
    try:
        for c in carpetas:
            print(f'Creando carpeta {c} en {rutaCarpeta}')
            mkdir(f'{rutaCarpeta}\{c}')
            print(f'Carpeta {c} creada correctamente')
    except OSError as e:
        print(e.strerror)
        if e.errno != errno.EEXIST:
            raise

def crear_archivo(carpeta, accion, complemento):
    clase = open(f'{carpeta_funcion}\{carpeta}\{accion}{complemento}.cs', 'w')
    new_name_space = f'{name_space}.{carpeta};\n\n'
    ctor = f'public {accion}{complemento}'
    nombre_clase_command = f'{accion}{complementos_command[0]}'
    nombre_clase_command_h = f'{accion}{complementos_command[1]}'
    nombre_clase_controller = f'{accion}{complementos[0]}'
    nombre_clase_response = f'{accion}{complementos[1]}'
    nombre_clase_query = f'{accion}{complementos_query[0]}'
    nombre_clase_query_h = f'{accion}{complementos_query[1]}'
    # Crear archivos Command
    if complemento == 'Command':
        clase.write(f'{u_mediat_r + n + new_name_space + p_record + nombre_clase_command}() : IRequest<{nombre_clase_response}>;')
    # Crear archivos CommandHandler    
    elif complemento == 'CommandHandler':
        clase.write(u_mediat_r + u_logica_negocio + n + new_name_space +
            f'{p_class}{nombre_clase_command_h} : IRequestHandler<{nombre_clase_command}, {nombre_clase_response}>{lla}' +
            f'{p_readonly + i_gestion} {c_gestion};{n + _ + ctor}({i_gestion} {v_gestion}) => {c_gestion} = {v_gestion};{n_n + _}' +
            f'{p_async_task}<{nombre_clase_response}> Handle({nombre_clase_command} request, {cancel_token}){lla2}' +
            f'{nombre_clase_response} result = await {c_gestion}.{accion}(request);{n_n + _*2}return result;{llc2 + llc}')
    # Crear archivos Controller
    elif complemento == 'Controller':
        a_http = '[HttpGet]' if carpeta != 'Crear' else '[HttpPost]'
        if carpeta == 'Editar': a_http = '[HttpPut]'
        parametro_send = nombre_clase_query + '()' if 'Consultar' in carpeta else nombre_clase_command + '()'
        clase.write(u_mediat_r + u_microsoft + n + new_name_space + a_route + a_controller +
            f'{p_class + nombre_clase_controller} : {complemento}Base{lla + p_readonly}IMediator _mediator;{n + _ + ctor + i_mediator_ctor + n + _}' +
            f'{a_http + a_resp + p_async_task}<IActionResult> {accion}(){lla2 + nombre_clase_response} response = await _mediator.Send(new ' +
            f'{parametro_send});{n_n + _*2}return Ok(response);{llc2 + llc}')
    # Crear archivos Response
    elif complemento == 'Response':
        clase.write(new_name_space + p_record + nombre_clase_response + '();')
    # Crear archivos Query
    elif complemento == 'Query' and carpeta == 'Consultar':
        clase.write(u_mediat_r + u_seg_comun + n + new_name_space + p_record + nombre_clase_query +
            f'(string textoBusqueda, int pagina, int registrosPorPagina) : IRequest<DataViewModel<{nombre_clase_response}>>;')
    elif complemento == 'Query' and carpeta == 'ConsultarPorId':
        clase.write(u_mediat_r + n + new_name_space + p_record + nombre_clase_query + f'(Guid Id) : IRequest<{nombre_clase_response}>;')
    # Crear archivos QueryHandler
    elif complemento == 'QueryHandler' and carpeta == 'Consultar':
        clase.write(u_mediat_r + u_seg_comun + u_logica_negocio + n + new_name_space + p_class + nombre_clase_query_h +
            f' : IRequestHandler<{nombre_clase_query}, DataViewModel<{nombre_clase_response}>>{lla + p_readonly + i_gestion} {c_gestion};' +
            f'{n + _ + ctor}({i_gestion} {v_gestion}) => {c_gestion} = {v_gestion};{n_n + _ + p_async_task}<DataViewModel<{nombre_clase_response}>> ' +
            f'Handle({nombre_clase_query} request, {cancel_token}){lla2}DataViewModel<{nombre_clase_response}> result = await {c_gestion}.{accion}' +
            f'(request.textoBusqueda, request.pagina, request.registrosPorPagina);{n_n + _*2}return result;{llc2 + llc}')
    elif complemento == 'QueryHandler' and carpeta == 'ConsultarPorId':
        clase.write(u_mediat_r + u_logica_negocio + n + new_name_space + p_class + nombre_clase_query_h +
            f' : IRequestHandler<{nombre_clase_query}, {nombre_clase_response}>{lla + p_readonly + i_gestion} {c_gestion};' +
            f'{n + _ + ctor}({i_gestion} {v_gestion}) => {c_gestion} = {v_gestion};{n_n + _ + p_async_task}<{nombre_clase_response}> ' +
            f'Handle({nombre_clase_query} request, {cancel_token}){lla2}{nombre_clase_response} result = await {c_gestion}.{accion}' +
            f'(request.Id);{n_n + _*2}return result;{llc2 + llc}')
    clase.close()

# Crea la carpeta para las funcionalidades de la entidad
crear_carpetas(ruta_proyecto, [entidad_plural])
# Crea las carpetas de funciones
crear_carpetas(carpeta_funcion, carpetas)

carpetas_logica = carpetas[-3:]  # Obtener los 3 últimos elementos
carpetas_accion = carpetas[:-3]  # Quitar los 3 últimos elementos

for c in carpetas_accion:
    if 'Consultar' in c:
        for com in complementos_query:
            accion = c + entidad_plural if c == 'Consultar' else f'Consultar{entidad_singular}PorId'
            crear_archivo(c, accion, com)
    else:
        for com in complementos_command:
            accion = c + entidad_singular
            crear_archivo(c, accion, com)

def crear_archivo_logica(carpeta, nombre_clase):
    clase = open(f'{carpeta_funcion}\{carpeta}\{nombre_clase}.cs', 'w')
    new_name_space = f'{name_space}.{carpeta};\n\n'
    ctor = f'public {nombre_clase}'
    # Crear Archivo Especificacion
    if carpeta == 'Especificacion':
        clase.write(f'using SEG.Comun.Especificacionbase;\n{u_seg_menu_entidades}{n}{new_name_space + p_class + nombre_clase} : SpecificationBase<{entidad_singular}>' +
            f'{lla + ctor}(string textoBusqueda, int? pagina = null, int? registrosPorPagina = null, string ordenarPor = null, string direccionOrdenamiento = "asc")' +
            f'{lla2}Criteria = BusquedaTextoCompleto(textoBusqueda).SatisfiedBy();{llc2 + n_n + _}private ISpecificationCriteria<{entidad_singular}> BusquedaTextoCompleto(string texto)' +
            f"{lla2}SpecificationCriteria<{entidad_singular}> especificacion = new SpecificationCriteriaTrue<{entidad_singular}>();{n_n + _*2}var spl = texto.ToLower().Trim().Split(' ');{n_n}" +
            f'{_*2}return especificacion;{llc2 + llc}')
    # Crear Archivos LogicaNegocio
    elif carpeta == 'LogicaNegocio':
        # Crear Interface de Gestion
        usings = ''
        for c in carpetas_accion:
            usings += f'{u_entidad}.{c};\n'
        interface = open(f'{carpeta_funcion}\{carpeta}\I{nombre_clase}.cs', 'w')
        interface.write(f'{u_seg_comun + usings + n + new_name_space + p_interface + i_gestion + lla}'
            f'Task<DataViewModel<Consultar{entidad_plural}Response>> Consultar{entidad_plural}(string filtro, int pagina, int registrosPorPagina,' + 
            f'string? ordenarPor = null, bool? direccionOrdenamientoAsc = null);{n + _}Task<Consultar{entidad_singular}PorIdResponse> Consultar{entidad_singular}PorId' +
            f'(Guid {entidad_singular_m}Id);{n + _}Task<Crear{entidad_singular}Response> Crear{entidad_singular}(Crear{entidad_singular}Command registroDto);{n + _}' +
            f'Task<Editar{entidad_singular}Response> Editar{entidad_singular}(Editar{entidad_singular}Command registroDto);{n + _}' +
            f'Task<ActivarInactivar{entidad_singular}Response> ActivarInactivar{entidad_singular}(Guid {entidad_singular_m}Id);{llc}')
        interface.close()
        # Crear Clase Gestion
        usings = ''
        for c in carpetas:
            if c != carpeta:
                usings += f'{u_entidad}.{c};\n'
        clase.write(f'using Ardalis.GuardClauses;\nusing SEG.Comun.ContextAccesor;\n{u_seg_comun + usings + u_seg_menu_entidades + u_unit_of_work + n}' +
            f'{new_name_space + p_class + nombre_clase} : BaseAppService, {i_gestion + lla + p_readonly + i_repo_lectura}_{v_repo_lectura};{n + _ + p_readonly}' +
            f'{i_repo_escritura}_{v_repo_escritura};{n + _ + p_readonly + i_unit_work_write} _unitOfWork;{n + _ + p_readonly}IContextAccessor _contextAccessor;' +
            f'{n_n + _ + ctor}({n + _*2 + i_repo_lectura + v_repo_lectura},{n + _*2 + i_repo_escritura + v_repo_escritura},{n + _*2 + i_unit_work_write}' +
            f'unitOfWork,{n + _*2}IContextAccessor contextAccessor,{n + _*2}ILoggerFactory loggerFactory{n + _*2}) : base(contextAccessor, loggerFactory)'+
            f'{lla2}_{v_repo_lectura} = {v_repo_lectura};{n + _*2}_{v_repo_escritura} = {v_repo_escritura};{n + _*2}_unitOfWork = unitOfWork;{n + _*2}'+
            f'_contextAccessor = contextAccessor;{llc2 + n + llc}')
    # Crear Archivos Respositorio
    elif carpeta == 'Repositorio':
        # Crear Interface Repositorio
        nombre_interface = 'I' + nombre_clase
        interface = open(f'{carpeta_funcion}\{carpeta}\{nombre_interface}.cs', 'w')
        interface.write(f'using SEG.Comun.Repositorios;\n{u_seg_menu_entidades + n + new_name_space + p_interface + nombre_interface} : ' +
            f'IRepositoryAsync<{entidad_singular}>{n}{{{n}}}')
        interface.close()
        # Crear Clase Repositorio
        clase.write(f'using SEG.Comun.Repositorios;\n{u_seg_menu_entidades + u_unit_of_work + n + new_name_space + p_class + nombre_clase} : ' +
            f'Repository<{entidad_singular}>, {nombre_interface + lla + ctor}({i_unit_work_write} unitOfWork) : base(unitOfWork){n + _}{{{n + _}}}{n}}}')
    clase.close()

for c in carpetas_logica:
    if c == 'Especificacion':
        nombre_clase = f'{entidad_singular}{c}'
        crear_archivo_logica(c, nombre_clase)
    elif c == 'LogicaNegocio':
        nombre_clase = f'Gestion{entidad_plural}'
        crear_archivo_logica(c, nombre_clase)
    elif c == 'Repositorio':
        for clase in clases_repo:
            nombre_clase = clase
            crear_archivo_logica(c, nombre_clase)

input('Presione cualquier tecla para cerrar la ventana...')


