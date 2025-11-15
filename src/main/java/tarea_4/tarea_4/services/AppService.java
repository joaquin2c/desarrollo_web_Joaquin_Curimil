package tarea_4.tarea_4.services;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.util.ResourceUtils;

import tarea_4.tarea_4.models.Aviso;
import tarea_4.tarea_4.models.AvisoRepository;
import tarea_4.tarea_4.models.Nota;
import tarea_4.tarea_4.models.NotaRepository;

@Service
public class AppService {

    private final String pathStatic;
    private final AvisoRepository avisoRepository;
    private final NotaRepository notaRepository;

    public AppService(AvisoRepository avisoRepository,NotaRepository notaRepository) throws IOException {
        this.avisoRepository = avisoRepository;
        this.notaRepository = notaRepository;
        // Dynamically resolve the absolute path for the static directory
        Path staticDir = Paths.get(ResourceUtils.getFile("classpath:static").getAbsolutePath());
        this.pathStatic = staticDir.toString();
        System.out.println("Static path resolved to: " + this.pathStatic);
    }

    public List<Map<String, String>> getAvisosData(Integer pageSize) {
        List<Aviso> avisos = avisoRepository.findAllByOrderByIdDesc(PageRequest.of(0, pageSize)).getContent();
        List<Map<String, String>> avisosData = new ArrayList<>();
        
        for (Aviso aviso : avisos) {
            Map<String, String> avisoData = new HashMap<>();
            avisoData.put("id", aviso.getId().toString());
            avisoData.put("fecha_ingreso", aviso.getFechaIngreso().toString());
            avisoData.put("sector", aviso.getSector());
            avisoData.put("cantidad", aviso.getCantidad().toString());
            avisoData.put("tipo", aviso.getTipo());
            avisoData.put("edad", aviso.getEdad().toString());
            avisoData.put("comuna", aviso.getComuna());
            avisoData.put("nota", aviso.getNota().toString());

            avisosData.add(avisoData);
        }
        return avisosData;
    }

    public void handlePostRequest(
        Integer nota,
        Integer aviso_id) throws Exception {

        if (Nota.validateNota(nota)) {
            
            System.out.println("New nota: " + nota);
            // Save the confession in the database
            Nota new_nota = new Nota();
            new_nota.setNota(nota);
            new_nota.setAviso(avisoRepository.findById(aviso_id).orElse(null));
            notaRepository.save(new_nota);
            System.out.println("Confession saved successfully.");
        } else {
            throw new IllegalArgumentException("Confession validation failed.");
        }
    }
}