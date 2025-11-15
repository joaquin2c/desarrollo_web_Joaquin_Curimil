package tarea_4.tarea_4.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import tarea_4.tarea_4.models.Aviso;
import tarea_4.tarea_4.models.AvisoRepository;
import tarea_4.tarea_4.services.ApiService;

@RestController
@RequestMapping("/avisos")
public class ApiController{
    private final ApiService apiService;
    public ApiController(ApiService apiService) {
        this.apiService = apiService;

    }
    @Autowired
    private AvisoRepository avisoRepository;

    @GetMapping("/all")
    @ResponseBody
    public Iterable<Aviso> getAllAvisos(){
        return avisoRepository.findAll();
    }

    @GetMapping("/{id}")
    public Aviso getAviso(@PathVariable Integer id){
        return avisoRepository.findById(id).orElse(null);
    }
}
