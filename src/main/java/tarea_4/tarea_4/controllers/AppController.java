package tarea_4.tarea_4.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import tarea_4.tarea_4.services.AppService;

@Controller
public class AppController {
    private final AppService appService;
    public AppController(AppService appService) {
        this.appService = appService;
    }


    @GetMapping("/")
    public String indexRoute(Model model) {
        /* 
        List<Map<String, String>> modelData = appService.getAvisosData(5);
        System.out.println("\ndata:\n");
        System.out.println(modelData);
        model.addAttribute("avisos_data", modelData);
        */
        return "listado";
    }

    @PostMapping("/post-nota")
    @ResponseBody
    public String postConfRoute(
        @RequestParam Integer nota,
        @RequestParam Integer aviso_id) throws Exception {
        appService.handlePostRequest(
            nota,
            aviso_id
        );

        return "redirect:/"; //redirects to indexRoute
    }

}