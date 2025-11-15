package tarea_4.tarea_4.models;

    
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AvisoRepository extends JpaRepository<Aviso, Integer> {
    Page<Aviso> findAllByOrderByIdDesc(Pageable pageable);
}