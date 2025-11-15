package tarea_4.tarea_4.models;
import java.time.LocalDateTime;
import java.util.List;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.PrimaryKeyJoinColumn;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;



@Entity
@Table(name = "aviso_adopcion")
public class Aviso {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @NotNull
    private LocalDateTime fecha_ingreso;

    @ManyToOne
    @PrimaryKeyJoinColumn(name = "comuna_id")
    Comuna comuna;

   
    @OneToMany(mappedBy = "aviso")
    private List<Nota> notas;


    private String sector;
    
    @NotNull
    private String nombre;
        
    @NotNull
    private String email;

    private String celular;
       
    @NotNull
    private String tipo;
        
    @NotNull
    private Integer cantidad;
        
    @NotNull
    private Integer edad;
        
    @NotNull
    private String unidad_medida;
        
    @NotNull
    private LocalDateTime fecha_entrega;
 
    private String descripcion;
    

    public Integer getId() {
        return id;
    }

    public LocalDateTime getFechaIngreso() {
        return fecha_ingreso;
    }

    public String getComuna() {
        return comuna.getNombre();
    }

    public String getSector() {
        return sector;
    }

    public String getNombre() {
        return nombre;
    }

    public String getEmail() {
        return email;
    }

    public String getCelular() {
        return celular;
    }

    public String getTipo() {
        return tipo;
    }

    public Integer getCantidad() {
        return cantidad;
    }

    public Integer getEdad() {
        return edad;
    }

    public String getUnidadMedida() {
        return unidad_medida;
    }

    public LocalDateTime getFechaEntrega() {
        return fecha_entrega;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public Double getNota() {
        Double nota=0.0;
        if(!notas.isEmpty()){
          for(Nota nota_cl : notas){
            nota+=nota_cl.getNota();
          }
          nota=nota/notas.size();
        }
        else{
          nota=0.0;
        }
        return nota;
    }
}