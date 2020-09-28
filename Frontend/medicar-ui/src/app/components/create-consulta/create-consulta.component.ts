
import { ChangeDetectionStrategy } from '@angular/core';
import { Component, OnInit } from '@angular/core';
import { NgForm, FormBuilder, AbstractControl, NgModel } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { Consulta } from 'src/app/_models/consulta';
import { ConsultaService } from 'src/app/_services/consulta.service';


@Component({
  selector: 'app-create-consulta',
  templateUrl: './create-consulta.component.html',
  styleUrls: ['./create-consulta.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CreateConsultaComponent{
  completedForm = false;
  consulta = {} as Consulta
  especialidadeList: any = []
  medicoList: any = []
  agendaList: any = []
  filteredAgendaList: any = []
  horarioList: any = []
  selectedEspecialidade: any = null;
  selectedMedico: any = null;
  selectedData: any = null;

  
  constructor(private consultaService: ConsultaService, public activeModal: NgbActiveModal, public formBuilder: FormBuilder) {}

  createConsultaForm = this.formBuilder.group({
    "agenda_id": '',
    "horario": ''
  })

  ngOnInit() {
    this.getEspecialidade();
  }

  onSubmit() {
    this.consulta = this.createConsultaForm.value;
    this.saveConsulta();
  }

  saveConsulta() {    
    this.consultaService.addConsulta(this.consulta).subscribe(() => {
      this.consulta = {} as Consulta;
      this.activeModal.close('Submit form')
    });
  }

  getEspecialidade() {
    this.consultaService.getEspecialidadeList().subscribe(
      (especialidadeList: Object) => {
        this.especialidadeList = especialidadeList['content'];
      }
    )
  }

  getMedicos(especialidade: number) {
    this.consultaService.getMedicoList(especialidade).subscribe(
      (medicoList: Object) => {
        this.medicoList = medicoList['content'];
      }
    )
  }

  getAgenda(especialidade: AbstractControl, medico: AbstractControl) {
    this.consultaService.getAgendaList(especialidade, medico).subscribe(
      (agendaList: Object) => {
        this.agendaList = agendaList['content'];
      }
    )
  }

  getAgendaByDate(date: AbstractControl, especialidade: AbstractControl, medico: AbstractControl) {
    this.consultaService.getAgendaListByDate(date, especialidade, medico).subscribe(
      (agendaList: Object) => {
        this.filteredAgendaList = agendaList['content'];
        this.filteredAgendaList.forEach(agenda => {
          agenda.horarios.forEach(horario => {
            if (!this.horarioList.includes(horario)) {
              this.horarioList.push(horario);
            }
          });
        });
      }
    )
  }

  changeEspecialidade(event, form: NgForm) {
    this.completedForm = false;
    form.resetForm();
    this.selectedData = null;
    this.selectedEspecialidade = null;
    this.selectedMedico = null;
    this.horarioList = [];
    this.agendaList = [];
    this.medicoList = [];
    this.selectedEspecialidade = event.target.value;
    this.getMedicos(event.target.value);
  }

  changeMedico(event, form: NgForm) {
    this.completedForm = false;
    form.resetForm();
    this.selectedData = null;
    this.selectedMedico = null;
    this.horarioList = [];
    this.agendaList = [];
    this.selectedMedico = event.target.value;
    this.getAgenda(
      this.selectedEspecialidade,
      this.selectedMedico   
    );
  }

  changeDia(event, form: NgForm) {
    this.completedForm = false;
    form.resetForm();
    this.horarioList = []
    this.selectedData = event.target.value;
    this.getAgendaByDate(
      this.selectedData,
      this.selectedEspecialidade,
      this.selectedMedico
    );
  }

  changeHorario(event) {
    this.completedForm = true;
    this.createConsultaForm.get('agenda_id').setValue(this.filteredAgendaList[0].id);
    this.createConsultaForm.get('horario').setValue(event.target.value);
  }
}
