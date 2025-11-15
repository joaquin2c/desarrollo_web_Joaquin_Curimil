package tarea_4.tarea_4.models;

import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import java.util.List;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;


@Entity
@Table(name = "comuna")

public class Comuna {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;


    @NotNull
    private String nombre;

    @NotNull
    private Integer region_id;

    @OneToMany(mappedBy = "comuna")
    private List<Aviso> avisos;



    public Integer getId() {
        return id;
    }


    public String getNombre() {
        return nombre;
    }

    public Integer getRegionId() {
        return region_id;
    }

     public List<Aviso> getAvisos() {
        return avisos;
    }
}
