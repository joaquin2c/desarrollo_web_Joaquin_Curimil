package tarea_4.tarea_4.services;

import org.springframework.stereotype.Service;

import tarea_4.tarea_4.models.AvisoRepository;

@Service
public class ApiService {
    private final AvisoRepository avisoRepository;
    public ApiService(AvisoRepository avisoRepository) {
        this.avisoRepository = avisoRepository;
    }
    
}