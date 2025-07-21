from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nume categorie")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, verbose_name="Descriere")
    icon = models.CharField(max_length=50, blank=True, help_text="Clasa CSS pentru iconiță (ex: fas fa-car)")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='subcategories', verbose_name="Categorie părinte")
    is_active = models.BooleanField(default=True, verbose_name="Activă")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categorii"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_full_path(self):
        """Returnează calea completă a categoriei (ex: Electronice > Telefoane)"""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name
