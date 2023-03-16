using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapPost("/submit", ([FromBody] JobMessage message) =>
{
  return Results.Ok();
});

app.Run();
