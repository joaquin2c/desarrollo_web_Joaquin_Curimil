package tarea_4.tarea_4.models;

import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.PrimaryKeyJoinColumn;

import java.time.LocalDateTime;

import org.springframework.web.multipart.MultipartFile;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;


@Entity
@Table(name = "nota")
public class Nota {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @NotNull
    private Integer nota;


    @ManyToOne
    @PrimaryKeyJoinColumn(name = "aviso_id")
    Aviso aviso;



    public Integer getId() {
        return id;
    }


    public Aviso getAviso() {
        return aviso;
    }


    public Integer getNota() {
        return nota;
    }

    public void setId(Integer id) {
        this.id=id;
    }


    public void setAviso(Aviso aviso) {
        this.aviso=aviso;
    }


    public void setNota(Integer nota) {
        this.nota=nota;
    }
    
    public static Boolean validateNota(Integer nota) {
        // Ejercicio: implementar validacion de confesiones :)
        return true;
    }
}
